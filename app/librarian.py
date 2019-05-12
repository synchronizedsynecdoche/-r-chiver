import archiveis
import time
import praw
import os
import prawcore.exceptions
import feedparser

class Librarian(object):

    global reddit

    def praw_auth(self):
        credentials = open("archiver.config")

        try:

            client_id = credentials.readline(-1).strip()
            client_secret = credentials.readline(-1).strip()
            password = credentials.readline(-1).strip()
            user_agent = credentials.readline(-1).strip()
            username = credentials.readline(-1).strip()
        except IOError:

            print("Caught an error!\nis your archiver.config file missing?")
            exit(1)

        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  password=password,
                                  user_agent=user_agent,
                                  username=username)

    def archive(self, url, num):

        base = "https://archive.today/download/"

        ar = archiveis.capture(url)

        if (num + 1) % 5 == 0:
            print("pausing to let the archiver catch up [ 20 seconds ]")
            time.sleep(20)

        print("[ %d ] " % num + ar)
        return str(ar)

    def comment_scrape(self, user, write_to_file=False, with_archive=False):

        returnable_bodies = []
        returnable_links = []
        returnable_archives = []
        try:
            if write_to_file:
                file = open("{}CommentCorpus.txt".format(user), "a")
        except IOError:

            print("Caught an Error!\nIOError")
            exit(1)

        reddit_base = "https://old.reddit.com/r/{}/{}"
        comment_IDs = []
        comment_subreddits = []
        wait_sentinel = 0
        try:

            for comment in self.reddit.redditor(user).comments.new(limit=None):

                returnable_bodies.append(comment.body + '\n')
                comment_IDs.append(comment.submission)
                comment_subreddits.append(comment.subreddit)

                if write_to_file:
                    file.write("[ {} ] ".format(wait_sentinel) + comment.body + "\n\n")

                wait_sentinel += 1

        except prawcore.exceptions.NotFound:

            print("Caught an error!\nUser {} not found!".format(user))

            if write_to_file:
                file.close()

            exit(1)

        wait_sentinel = 0
        for cid in comment_IDs:
            print("[ %d ] " % wait_sentinel + reddit_base.format(comment_subreddits[wait_sentinel],
                                                                 comment_IDs[wait_sentinel]))

            returnable_links.append(reddit_base.format(comment_subreddits[wait_sentinel],
                                                       comment_IDs[wait_sentinel]))

            if write_to_file:
                file.write("[ {} ] ".format(wait_sentinel) + reddit_base.format(comment_subreddits[wait_sentinel],
                                                                     comment_IDs[wait_sentinel]) + "\n")
            if with_archive:

                returnable_archives.append(self.archive(reddit_base.format(comment_subreddits[wait_sentinel],
                                           comment_IDs[wait_sentinel]), wait_sentinel))
                if write_to_file:
                    file.write("[ {} ] ".format(wait_sentinel) + returnable_archives[wait_sentinel] + "\n")
            wait_sentinel += 1


        if write_to_file:
            file.close()
        return returnable_bodies, returnable_links, returnable_archives

    def submission_scrape(self, user, write_to_file=False, with_archive=False):

        returnable_bodies = []
        returnable_links =[]
        returnable_archives = []
        try:

            if write_to_file:
                file = open("{}SubmissionCorpus.txt".format(user), "a")
        except IOError:

            print("Caught an Error!\nIOError")
            exit(1)

        reddit_base = "https://old.reddit.com/r/{}/{}"
        submission_IDs = []
        submission_subreddits = []
        try:

            for submission in self.reddit.redditor(user).submissions.new(limit=None):

                returnable_bodies.append(submission.selftext)
                submission_IDs.append(submission)
                submission_subreddits.append(submission.subreddit)

                if write_to_file:
                    file.write(submission.title + "\n")
                    file.write(submission.selftext + "\n")

            if write_to_file:
                file.close()

        except prawcore.exceptions.NotFound:

            print("Caught an error!\nUser {} not found!".format(user))

            if write_to_file:
                file.close()
            exit(1)

        wait_sentinel = 0
        for sid in submission_IDs:

            returnable_links.append(reddit_base.format(submission_subreddits[wait_sentinel],
                                                       submission_IDs[wait_sentinel]))
            if with_archive:

                returnable_archives.append(self.archive(reddit_base.format(submission_subreddits[wait_sentinel],
                                                                           submission_IDs[wait_sentinel]), wait_sentinel))

            wait_sentinel += 1

        return returnable_bodies, returnable_links, returnable_archives
