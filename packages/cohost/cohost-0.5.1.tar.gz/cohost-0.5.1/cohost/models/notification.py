from typing import Any


class BaseNotification:
    def __init__(self, createdAt, fromProject):
        self.createdAt = createdAt
        self.fromProject = fromProject

    @property
    def timestamp(self):
        return self.createdAt


class Like(BaseNotification):
    def __init__(self, createdAt, fromProject, toPost, relationshipId):
        super().__init__(createdAt, fromProject)
        self.toPost = toPost
        self.relationshipId = relationshipId

    def __str__(self) -> str:
        return "{} liked {} | {}".format(
            self.fromProject.handle,
            self.toPost.postId,
            self.timestamp
        )


class Share(BaseNotification):
    def __init__(self, createdAt, fromProject,
                 toPost, sharePost, transparentShare):
        super().__init__(createdAt, fromProject)
        self.toPost = toPost
        self.sharePost = sharePost
        self.transparentShare = transparentShare

    def __str__(self) -> str:
        if self.transparentShare:
            return "{} shared {} | {}".format(
                self.fromProject.handle,
                self.toPost.postId,
                self.timestamp
            )
        return "{} shared {} with extra | {}".format(
            self.fromProject.handle,
            self.toPost.postId,
            self.timestamp
        )


class Comment(BaseNotification):
    def __init__(self, createdAt, fromProject, toPost, comment, inReplyTo):
        super().__init__(createdAt, fromProject)
        self.toPost = toPost
        self.comment = comment
        self.inReplyTo = inReplyTo

    def __str__(self) -> str:
        if self.toPost is None:
            return (f"{self.fromProject.handle} commented on " +
                    "[post that couldn't be retrieved]- " +
                    f"\"{self.comment.body}\" | {self.timestamp}")
        return "{} commented on {} - \"{}\" | {}".format(
            self.fromProject.handle,
            self.toPost.postId,
            self.comment.body,
            self.timestamp
        )


class Follow(BaseNotification):
    def __init__(self, createdAt, fromProject):
        super().__init__(createdAt, fromProject)

    def __str__(self) -> str:
        return "{} is now following you | {}".format(
            self.fromProject.handle,
            self.timestamp
        )


"""Unwrap a raw notification list's grouped notifications


    Returns:
        list: unwrapped notification list
"""


def unwrapGroupedNotifications(notificationsRaw: dict):
    unwrapped = []
    # Unwrap any grouped notifications
    for notif in notificationsRaw:
        if not notif['type'].startswith('grouped'):
            unwrapped.append(notif)
            continue
        # Ok, this is guaranteed to be wrapped
        for i in range(0, len(notif['fromProjectIds'])):
            fromProjectId = notif['fromProjectIds'][i]
            # If this is None, this means the code later will ignore it
            relationshipId = None
            sharePostId = None
            if notif['type'] == 'groupedLike':
                relationshipId = notif['relationshipIds'][i]
            if notif['type'] == 'groupedShare':
                sharePostId = notif['sharePostIds'][i]
            unwrapped.append({
                'type': notif['type'].replace('grouped', '').lower(),
                'fromProjectId': fromProjectId,
                'relationshipId': relationshipId,
                'sharePostId': sharePostId,
                'createdAt': notif['createdAt'],
                'toPostId': notif.get('toPostId', None),
                'transparentShare': notif.get('transparentShare', None)
            })
    return unwrapped


def buildFromNotifList(notificationsApiResp: dict[str, Any], user):
    from cohost.models.comment import Comment as CommentModel
    from cohost.models.post import Post  # noqa: F401
    from cohost.models.user import User  # noqa: F401
    u = user
    user = u  # this gets intellisense working without circular imports
    # I Love Python
    # We need the user to do API operations upon
    # It helps us resolve things like projects!
    commentsRaw = notificationsApiResp.get('comments', [])
    postsRaw = notificationsApiResp.get('posts', [])
    projectsRaw = notificationsApiResp.get('projects', [])
    notificationsRaw = notificationsApiResp.get('notifications', [])
    # Ok, so, now we HAVE all of this, we can build the notifications
    # First step: projects
    projects = []
    for p in projectsRaw:
        projects.append(user.resolveSecondaryProject(projectsRaw[p]))
    # OK, now we have projects, we can build the posts
    posts = []
    for p in postsRaw:
        # first, let's find the project
        p = postsRaw[p]
        found = False
        for project in projects:
            if project.projectId == p['postingProject']['projectId']:
                found = True
                break
        if not found:
            project = user.resolveSecondaryProject(p['postingProject'])
        posts.append(Post(p, project))
    # OK, now we have posts, we can build the comments
    commentQueue = []
    for c in commentsRaw:
        commentQueue.append(commentsRaw[c])
    comments: list[CommentModel] = []
    while len(commentQueue) > 0:
        nextNotif = commentQueue.pop(0)
        if nextNotif.get('attemptsToProcess', 0) == 0:
            nextNotif['attemptsToProcess'] = 0
        replyComment = None
        if nextNotif['comment']['inReplyTo']:
            found = False
            for n in comments:
                if n.id == nextNotif['comment']['inReplyTo']:
                    found = True
                    replyComment = n
                    break
            # we still have other notifications to be processed
            nextNotif['attemptsToProcess'] += 1
            if (not found and len(commentQueue) > 0
                    and (not nextNotif['attemptsToProcess'] > 50)):
                commentQueue.append(nextNotif)
                continue
        # Ok, sick, so, we either don't have a reply
        # ... or we do but it's already processed!
        # we need pull the Project for this comment
        posterProject = None
        for project in projects:
            if project.projectId == nextNotif['poster']['projectId']:
                posterProject = project
        c = CommentModel(nextNotif['canEdit'], nextNotif['canInteract'],
                         nextNotif, posterProject, user, replyComment)
        comments.append(c)
    # Unwrap grouped notifications
    # a "grouped" notif will cause breaking behaviour to older tools
    notificationsRaw = unwrapGroupedNotifications(notificationsRaw)
    # and NOW we can finally map our notifications to all of our data models
    # TODO: Build notification model
    notifications: list[Like | Share | Comment | Follow] = []
    for notification in notificationsRaw:
        # first, let's resolve all the data back
        fromProject = None
        toPost = None
        sharePost = None
        comment = None
        inReplyTo = None
        if notification.get('fromProjectId'):
            for project in projects:
                if project.projectId == notification['fromProjectId']:
                    fromProject = project
                    break
        if notification.get('toPostId'):
            for post in posts:
                if post.postId == notification['toPostId']:
                    toPost = post
                    break
        if notification.get('sharePostId'):
            for post in posts:
                if post.postId == notification['sharePostId']:
                    sharePost = post
                    break
        if notification.get('commentId'):
            for c in comments:
                if c.id == notification['commentId']:
                    comment = c
                    break
        if notification.get('inReplyToId'):
            for c in comments:
                if c.id == notification['inReplyToId']:
                    inReplyTo = c
                    break
        # sick, we can now handle whichever type of notification this is
        if notification['type'] == 'like':
            notifications.append(
                Like(
                    notification['createdAt'],
                    fromProject,
                    toPost,
                    notification['relationshipId']
                )
            )
        if notification['type'] == "share":
            notifications.append(
                Share(
                    notification['createdAt'],
                    fromProject,
                    toPost,
                    sharePost,
                    notification['transparentShare']
                )
            )
        if notification['type'] == "comment":
            notifications.append(
                Comment(
                    notification['createdAt'],
                    fromProject,
                    toPost,
                    comment,
                    inReplyTo
                )
            )
        if notification['type'] == 'follow':
            notifications.append(
                Follow(notification['createdAt'], fromProject)
            )
    return notifications
