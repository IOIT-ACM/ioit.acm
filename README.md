# IOIT ACM Student Chapter Flask Project

This is a Flask project for the IOIT ACM Student Chapter website. Tech stack for this site includes Flask, HTMX, TailwwindCSS, [sheetdb](https://sheetdb.io/)

![Home page](./docs/home.png)
_Home page_
![Membership](./docs/membership.png)
_Membership Status_
![Footer](./docs/footer.png)
_Footer_

## dependencies

1. Python

```
pip install -r requirements.txt
```

2. TailwindCSS (run `npm install`)

```
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/tailwind.css --watch
```

## data

1. Teams
   The `app/data/teams.py` file contains information about the members of the IOIT ACM committee, organized by year.

2. Events
   The `app/data/events.py` file contains a list of events organized by name, description, and date. Here's the structure:

## build.sh

Currently, there is no Git integration in this project. However, the `build.sh` file located in the root directory serves as a utility to copy the necessary project files to a specified destination directory (`$DEST_DIR`). These files can then be zipped and uploaded to cPanel for hosting.

### Instructions:

1. **Set the Destination Directory**
   Modify the `$DEST_DIR` variable in the script to specify the desired location where the project files will be copied.

2. **Make the Script Executable** (Optional)
   To ensure that the script is executable, you can run the following command:

   ```bash
   chmod +x build.sh
   ```

3. **Run the Script**
   After making the script executable, run it with:
   ```bash
   ./build.sh
   ```

## Available Routes

The following routes are available in the project:

- [x] **`/`**: The home page of the site.
- [ ] **`/about`**: The about page.
- [x] **`/membership`**: The membership page.
- [x] **`/membership/status`**: A page showing membership status.
- [ ] **`/gallery`**: A page (currently under development) displaying images or events.
- [x] **`/team`**: A page with details of the IOIT ACM committee members.
- [x] **`/events`**: A page displaying upcoming events.

## TO-DOs

- Collect team images
- About page
- Gallery page
- Search feature on `/membership/status` page
