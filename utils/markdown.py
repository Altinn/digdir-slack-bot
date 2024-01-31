import pprint

block_token = "```"
section_delimiter = '\n\n'

def block_token_count(markdown: str):
  return markdown.count(block_token)

def has_open_code_block(markdown: str):
  return block_token_count(markdown) % 2 == 1

def split_to_sections(markdown: str):
    if markdown is None:
        return []
    
    sections = markdown.split(section_delimiter)
    # print(len(sections))
    # print('Sections before merging')
    # log_sections(sections)


    for i in range(len(sections)):
        if has_open_code_block(sections[i]):
            if i < (len(sections) - 1):
                print(f'Merging section {i} and {i+1}')
                sections[i] = sections[i] + section_delimiter + sections[i+1]
                sections[i+1] = ""

    # print('Sections before filtering')
    # log_sections(sections)

    sections = list(filter(None, sections))
    
    # print(f'Final section list')
    # log_sections(sections)

    return sections


def is_null_or_empty(input_str):
    if input_str:
        return False
    else:
        return True

def log_sections(sections):
   for i in range(len(sections)):
      print(f"{i}: {sections[i]}")


if __name__ == "__main__":
  test_md = """Based on the information provided, Altinn 3 supports sending notifications through two channels: email and SMS. Notifications can be triggered based on the state of, or actions performed on, an Altinn App instance. For instance, when the next stage in a process is successful, a notification can be sent to inform the users.

Here is an example of a standard notification order that could be used to send an email notification:
```json
{
 "id": "a56c0933-d609-4b5c-a5da-bccfd407c9b8",
 "creator": "ttd",
 "sendersReference": "test-2023-1",
 "requestedSendTime": "2024-01-02T13:49:31.5591909Z",
 "created": "2024-01-02T13:49:31.5799658Z",
 "notificationChannel": "Email",
 "recipients": [
  {
   "emailAddress": "testuser_1@altinn.no"
  },


  {
   "emailAddress": "testuser_2@altinn.no"
  }
 ],
 "emailTemplate": {
  "fromAddress": "noreply@altinn.cloud",
  "subject": "A test email from Altinn Notifications",
  "body": "A message sent from an application owner through Altinn.",
  "contentType": "Html"
 },
 "links": {
  "self": "https://platform.at22.altinn.cloud/notifications/api/v1/orders/a56c0933-d609-4b5c-a5da-bccfd407c9b8",
  "status": "https://platform.at22.altinn.cloud/notifications/api/v1/orders/a56c0933-d609-4b5c-a5da-bccfd407c9b8/status"
 }
}
```

This JSON structure represents a notification order that requests the sending of an email to two recipients. The notification includes details such as the sender's reference, the requested send time, the channel to be used (in this case, Email), and the content of the email.
To implement notifications that are triggered by process events, you would need to integrate the notification service into your Altinn App workflow. This could involve setting up conditions related to the state of the Altinn App instance and using the Notifications API to create and send the notific…
For more detailed guidelines on how to use Altinn Notifications, you can refer to the user guide provided in the Altinn documentation, which is a work in progress. The existing guidelines for sending notifications through Altinn 2 also apply to Altinn Notifications."""

  sections = split_to_sections(test_md)

  log_sections(sections)