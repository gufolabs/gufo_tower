
# Python modules
import logging
import os
import shutil

logger = logging.getLogger(__name__)


def check_destination(self, dest, url, rev_options, rev_display):
    """
    Prepare a location to receive a checkout/clone.

    Return True if the location is ready for (and requires) a
    checkout/clone, False otherwise.
    """
    checkout = True
    if os.path.exists(dest):
        checkout = False
        if os.path.exists(os.path.join(dest, self.dirname)):
            existing_url = self.get_url(dest)
            if self.compare_urls(existing_url, url):
                logger.debug(
                    '%s in %s exists, and has correct URL (%s)',
                    self.repo_name.title(),
                    dest,
                    url,
                )
                if not self.check_version(dest, rev_options):
                    logger.info(
                        'Updating %s %s%s',
                        dest,
                        self.repo_name,
                        rev_display,
                    )
                    self.update(dest, rev_options)
                else:
                    logger.info(
                        'Skipping because already up-to-date.')
            else:
                logger.warning(
                    '%s %s in %s exists with URL %s',
                    self.name,
                    self.repo_name,
                    dest,
                    existing_url,
                )
        else:
            logger.warning(
                'Directory %s already exists, and is not a %s %s.',
                dest,
                self.name,
                self.repo_name,
            )
            shutil.rmtree(dest)
            checkout = True
    return checkout


def unpack(self, location, url):
    """
    monkey patch pip library cause they always remove downloaded dir. no idea why
    """
    self.obtain(location, url=url)
