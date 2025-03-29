# Meetup AutoRSVP

A command line tool to automatically RSVP to events from specified groups on Meetup.com.

## Overview

Meetup AutoRSVP is a Python-based command line tool designed to streamline your event management on Meetup.com. It helps you manage your groups, view events, and automatically RSVP to events based on your selected conditions.

## Features

- List Joined Groups: View all Meetup groups you are currently a member of.

- Display Events: See all upcoming events across your groups.

- Automatic RSVP: Automatically RSVP to events in selected groups when conditions are met.

## How it works

1. Cookies for meetup.com are extracted from your browser
2. Required data is scraped by sending GraphQL queries with those cookies
3. Complex json data is structured into simple data models
4. User is shown the data in tabular form

## Installation

Follow these steps to get started:

1. Clone the Repository
   ```sh
   git clone https://github.com/Ahmedazim7804/meetup_auto_rsvp
   ```
2. Change to project directory
   ```sh
   cd meetup_auto_rsvp
   ```
3. Install the project
   ```sh
   poetry install
   ```
4. Run the project
   ```sh
   poetry run meetup --help
   ```

## Basic Usage

1. Login to meetup.com in any of these browsers

   - Firefox
   - Chrome
   - Safari
   - Edge
   - Brave

   `Note: If you are logged into multiple browsers, the selection will be based on the priority order in this list.`

2. Setup the config file

   ```sh
   poetry run meetup config
   ```

3. Auto Rsvp to all events of selected groups in config
   ```sh
   poetry run meetup rsvp --all
   ```

## TODO

1. Allow selecting the preferred browser in config
2. Feature to check login state of user on meetup.com
3. Feature to get list of events of a group by its url/name
4. Refactor main.py

## License

This project is licensed under the MIT License. See the LICENSE file for details.
