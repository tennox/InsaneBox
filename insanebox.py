""" This could someday be a opensource alternative to SaneBox
"""

__author__ = 'TeNNoX'
__email__ = 'kai-manuel@web.de'

from imapwrapper import IMAPWrapper

def main():
    with IMAPWrapper() as wrapper:
        wrapper.select_folder('INBOX')
        messages = wrapper.client.search(['NOT DELETED'])

        wrapper.add_question("Question 1", "Test question.")


if __name__ == "__main__":
    main()

