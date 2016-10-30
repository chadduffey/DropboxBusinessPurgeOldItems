import datetime
import dropbox
import logging

#---------------------------------------------------------------------------
# Modify
#---------------------------------------------------------------------------
MAX_CONTENT_AGE = 100
DISPLAY_ONLY_MODE = True
TOKEN = "YOUR-DROPBOX-BUSINESS-TEAM-MEMBER-FILE-ACCESS-TOKEN"
LOG_NAME = "dropboxpurge.log"
#---------------------------------------------------------------------------


dbx = dropbox.DropboxTeam(TOKEN)
MAX_AGE = datetime.timedelta(days=MAX_CONTENT_AGE)
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename=LOG_NAME, format=FORMAT, level=logging.INFO)



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log_init():
    logging.info("Begin pass...")
    logging.info("MAX_CONTENT_AGE: {}".format(MAX_CONTENT_AGE))
    logging.info("DISPLAY_ONLY_MODE: {}".format(str(DISPLAY_ONLY_MODE)))


def retrieve_member_list(recursive=True):
    logging.info("retrieve_member_list (recursive={}".format(str(recursive)))

    all_members = []
    members = dbx.team_members_list()
    all_members.extend(members.members)
    if recursive:
        while members.has_more:
            print("(retrieving another 1000 users)")
            logging.info("(retrieving another 1000 users)")
            members = dbx.team_members_list_continue(members.cursor)
            all_members.extend(members.members)

    logging.info("member list obtained - {} members".format(len(all_members)))
    return all_members


def dropbox_content(member_id):
    logging.info("retrieving content for {}".format(member_id))
    content_listing = []
    result = dbx.as_user(member_id).files_list_folder(path="",
                                                        recursive=True,
                                                        include_media_info=False,
                                                        include_deleted=False,
                                                        include_has_explicit_shared_members=False)
    content_listing.extend(result.entries)
    while result.has_more:
        result = dbx.as_user(member_id).files_list_folder_continue(result.cursor)
        content_listing.extend(result.entries)

    logging.info("retrieved content for {}".format(member_id))
    return content_listing


def display_content(content):
    for item in content:
        if type(item) == dropbox.files.FileMetadata:
            last_touch_date = item.client_modified if item.client_modified > item.server_modified else item.server_modified
            if last_touch_date.date() > (datetime.date.today() - MAX_AGE):
                print("\t{0} ({1})".format(item.path_lower, last_touch_date))
                logging.info("{} would not have been deleted".format(item.path_lower))
            else:
                print(bcolors.FAIL + "\t{0} ({1})".format(item.path_lower, last_touch_date) + bcolors.ENDC)
                logging.info("{} would have been deleted".format(item.path_lower))


def delete_content(content, member_id):
    for item in content:
        if type(item) == dropbox.files.FileMetadata:
            last_touch_date = item.client_modified if item.client_modified > item.server_modified else item.server_modified
            if last_touch_date.date() > (datetime.date.today() - MAX_AGE):
                print("Ignoring:\t{}".format(item.path_lower))
                logging.info("Ignored: {}".format(item.path_lower))
            else:
                print(bcolors.FAIL + "Deleting:\t{}".format(item.path_lower) + bcolors.ENDC)
                logging.info("Attempting to delete: {}".format(item.path_lower))
                delete(member_id, item.path_lower)


def delete(member_id, path):
    try:
        result = dbx.as_user(member_id).files_delete(path)
        if type(result) == dropbox.files.DeleteError:
            print("Problem deleting {}".format(path))
            logging.info("Tried to delete: {} but couldn't".format(path))
        else:
            print("deleted {}".format(path))
            logging.info("Deleted: {}".format(path))
    except dropbox.exceptions.ApiError:
        print("Problem deleting {}".format(path))
        logging.info("Tried to delete: {} but couldn't".format(path))


if __name__ == "__main__":
    log_init()
    for team_member in retrieve_member_list():
        if team_member.profile.status == dropbox.team.TeamMemberStatus.active:
            print(bcolors.BOLD + 'Team Member:\t{}'.format(team_member.profile.email) + bcolors.ENDC)
            content = dropbox_content(team_member.profile.team_member_id)
            if DISPLAY_ONLY_MODE:
                display_content(content)
            elif not DISPLAY_ONLY_MODE:
                delete_content(content, team_member.profile.team_member_id)







