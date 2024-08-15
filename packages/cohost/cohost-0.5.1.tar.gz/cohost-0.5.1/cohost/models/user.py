import base64
from hashlib import pbkdf2_hmac
from typing import Any, Optional

from cohost.models.notification import buildFromNotifList
from cohost.models.project import EditableProject
from cohost.network import fetch, fetchTrpc, generate_login_cookies


class User:
    def __init__(self, cookie) -> None:
        self.cookie = cookie

    def __str__(self) -> str:
        return "user_{}".format(self.userId)

    @property
    def email(self) -> str:
        return self.userInfo['email']

    @property
    def userId(self) -> str:
        return self.userInfo['userId']

    @property
    def modMode(self) -> bool:
        return self.userInfo['modMode']

    @property
    def activated(self) -> bool:
        return self.userInfo['activated']

    @property
    def readOnly(self) -> bool:
        return self.userInfo['readOnly']

    @property
    def defaultProject(self) -> EditableProject:
        from cohost.models.project import EditableProject
        return EditableProject(self, self.userInfo['projectId'])

    @property
    def userInfo(self) -> dict:
        return fetchTrpc('login.loggedIn', self.cookie)['result']['data']

    """Fetch data from the API about projets the user can edit

    Returns:
        dict: Project dictionaries
    """
    @property
    def editedProjectsRaw(self) -> list[dict[str, Any]]:
        rawResp = fetchTrpc('projects.listEditedProjects', self.cookie)
        return rawResp['result']['data']['projects']

    """Fetch data from the API about projects the user can edit

    Returns:
        list[Project]: Project objects
    """
    @property
    def editedProjects(self) -> list:
        rawP = self.editedProjectsRaw
        projects = []
        for project in rawP:
            projects.append(EditableProject(self, project['projectId']))
        return projects

    """Get a salt for an email - for use in logging in


    Returns:
        str: Base64 encoded salt
    """
    @staticmethod
    def getSalt(email):

        salt = fetch(
            "GET",
            "/login/salt",
            {'email': email}
        )
        return salt

    """Create a user object from a login and password"""
    @staticmethod
    def login(email, password):
        # base64 terribleness
        salt = fetch("GET", "/login/salt", {"email": email})['salt']
        # explanation for whatever this is by @iliana
        # https://cohost.org/iliana/post/180187-eggbug-rs-v0-1-3-d
        salt = salt.replace('-', 'A')
        salt = salt.replace('_', 'A')
        salt = salt + "=="

        saltDecoded = base64.b64decode(salt.encode("ascii"))

        # generating the hash
        # the 200000 is the magic iter number - Use This, or login will break
        hash = pbkdf2_hmac("sha384", password.encode("utf-8"), saltDecoded,
                           200000, 128)
        clientHash = base64.b64encode(hash).decode("ascii")

        # getting cookie
        res = fetch("POST", "/login",
                    {"email": email, "clientHash": clientHash}, complex=True)
        sessionCookie = (res['headers']['set-cookie'].
                         split(";")[0].split("=")[1])

        u = User(sessionCookie)
        # if no error we're good
        u.userInfo
        return u

    """Create a user object from a cookie"""
    @staticmethod
    def loginWithCookie(cookie):
        # First, let's create a user
        u = User(cookie)
        # Now, we need to validate functions are working
        # We can do this by getting the user's info
        u.userInfo
        # If this didn't error out, we're good!
        return u

    def getProject(self, handle: str) -> Optional[EditableProject]:
        # Retrieve a project that you can edit
        projects = self.editedProjects
        for project in projects:
            if project.handle == handle:
                return project
        return None

    def resolveSecondaryProject(self, projectData):
        from cohost.models.project import Project
        editableProjects = self.editedProjects
        for project in editableProjects:
            if project.projectId == projectData['projectId']:
                return project
        return Project(self, projectData)

    @property
    def notifications(self):
        return self.notificationsPagified(notificationsPerPage=10)

    @property
    def allNotifications(self):
        page = 0
        notifsPerPage = 100
        notifs = self.notificationsPagified(
            page=page,
            notificationsPerPage=notifsPerPage
        )
        newNotifs = notifs
        while len(newNotifs) == notifsPerPage:
            page += 1
            newNotifs = self.notificationsPagified(
                page=page,
                notificationsPerPage=notifsPerPage
            )
            for n in newNotifs:
                notifs.append(n)
        return notifs

    def notificationsPagified(self, page=0, notificationsPerPage=10):
        nJson = self.notificationsRaw(page, notificationsPerPage)
        return buildFromNotifList(nJson, self)

    def notificationsRaw(self, page=0, notificationsPerPage=10):
        return fetch('GET', 'notifications/list', {
            'offset': page * notificationsPerPage,
            'limit': notificationsPerPage
        }, generate_login_cookies(self.cookie))
