<h1 align="center">Welcome to notion-heroku 👋</h1>
<p align="center">
  <a href="https://github.com/kevinjalbert/notion-heroku/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg" target="_blank" />
  </a>
  <a href="https://twitter.com/kevinjalbert">
    <img alt="Twitter: kevinjalbert" src="https://img.shields.io/twitter/follow/kevinjalbert.svg?style=social" target="_blank" />
  </a>
</p>

> Heroku hosted application that performs [Notion](https://www.notion.so/) actions (i.e., new task, new note) based on voice requests via [IFTTT Webhooks](https://ifttt.com/maker_webhooks) and [Google Assistant](https://ifttt.com/google_assistant).

## Prerequisites

1. Have a [Notion](https://www.notion.so/) account
2. Have a [Heroku](https://heroku.com/) account
3. Have an [IFTTT](https://ifttt.com/) account (with Google Assistant service enabled)
4. ~~Have [Specific Notion Template](https://www.notion.so/Week-Template-0a7ac4d03082417c929176b5ea1df07e) as described in [this blog post](https://kevinjalbert.com/my-weekly-notion-setup/)~~ Have a table for Notes and/or a table for Tasks (can be the same table)
5. Your Notion Token
6. URLs for the tables defined in 4.

## Install

_Note:_ The required environment variables mentioned in the below steps are outlined in [kevinjalbert/alfred-notion](https://github.com/kevinjalbert/alfred-notion)'s section on [finding your Notion Token](https://github.com/kevinjalbert/alfred-notion#finding-your-notion-token) and [finding your Notion URLs](https://github.com/kevinjalbert/alfred-notion#finding-your-notion-urls).

### Environment Variables

- NOTION_TOKEN = [your Notion Token](https://github.com/kevinjalbert/alfred-notion#finding-your-notion-token)
- NOTES_DATABASE_URL = the url to your notes database
- TASKS_DATABASE_URL = the url to your tasks database (can be the same)
- MAX_TITLE_LENGTH (optional) = the maximum length of the title before it gets truncated. If your title gets truncated, the full, untruncated title will first be added to the database row's page as a text block, so you won't lose any text. Defaults to 100 characters.

### With Heroku Deploy Button
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

1. Use above deploy button to create/launch application on [Heroku](https://heroku.com/)
2. Navigate to application settings page (i.e., https://dashboard.heroku.com/apps/your-notion-heroku/settings) and set required environment variables.

### Manually

1. Clone the repository via `git clone git@github.com:kevinjalbert/notion-heroku.git`
2. `heroku create`
3. `git push heroku master`
4. Set all required environment variables via `heroku config:set xxxx=yyyy`

### Setting up IFTTT Actions

<details><summary>Click to view walkthrough (images)</summary>

<br>

This walkthrough demonstrates how to setup a IFTTT action to add a Notion Task.

The main difference is that the webhook URL is either `/add_note` or `/add_task` in Step 6.

#### Step 1 - Choose _Trigger_ Service (Google Assistant)

![Step 1](./step1.png)

#### Step 2 - Choose Google Assistant Trigger

![Step 2](./step2.png)

#### Step 3 - Complete Google Assistant Trigger Fields

![Step 3](./step3.png)

#### Step 4 - Choose _Action_ Service (Webhooks)

![Step 4](./step4.png)

#### Step 5 - Choose Webhooks Action

![Step 5](./step5.png)

#### Step 6 - Complete Webhook Action Fields

![Step 6](./step6.png)

</details>

## Notes: ##
ThI haven't updated the above screenshots from [@kevinjalbert](https://github.com/kevinjalbert)'s original versions. While I've made sure you can still use the `?title=` parameter, you can also omit that if you send JSON in the request body.

If the JSON object is present, it will extract a `"title"` from that, and anything in the `"body"` property will be put into the database row's page. Any other properties you supply in this object will automatically map to other database properties if present, and if not return an error indicating which properties were not present.

This opens up opportunities to include information like the source of your note (e.g. Google Assistant, Email, etc) if you set up multiple IFTTT trigger sources, or to add any other contextual information you deem relevant.

### Example
    
    {
      "title": "<Row title>", // REQUIRED. The title of the database row you're creating
      "type": "Note"|"Task",  // Which of the databases you want it to go to
      "url": "<url>",         // The url of the database you want it to go to (overrides "type")
      "body": "<text>"        // Text block you want to create inside the row's page (Markdown supported)
    }

## Author

👤 **Kevin Jalbert**

* Twitter: [@kevinjalbert](https://twitter.com/kevinjalbert)
* Github: [@kevinjalbert](https://github.com/kevinjalbert)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
