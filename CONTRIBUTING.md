# Contributing to CeleryViz

## Welcome to the Project! 🎉

Hey there! We are **thrilled** that you're thinking about contributing to our project. Your ideas, code, and feedback help make this even better, and we're excited to see what you'll bring to the table! 😄


## How to Get Started 🚀

Contributing is easy! Just follow these steps:


### Reporting Bugs

If you find a bug, please open an issue on GitHub with the following information:
- A clear and descriptive title.
- A detailed description of the problem, including steps to reproduce.
- Any relevant logs or screenshots.


### Suggesting Features

Got a wild idea? We want to hear it! Don’t hesitate to suggest cool new features or improvements. 🌈💡

Open an issue on GitHub with the following information:
- A clear and descriptive title.
- A detailed description of the enhancement, including use cases and benefits.


### Where to report
  - If the issue to be reported is on the frontend, report it on [celeryviz_frontend_core](https://github.com/bhavya-tech/celeryviz_frontend_core/issues)

  - If the issue to be reported is in the python library, report it on this repository. ([celeryviz](https://github.com/bhavya-tech/celeryviz))


### Submitting Pull Requests

1. 🍴 **Fork the repository**  
   Make a copy of this project under your GitHub account. You can do this by clicking the **Fork** button at the top right of the repo page.

2. 🖇️ **Clone your forked repository**

    Time to get the code on your local machine! Run this command:

    ```bash
    git clone https://github.com/your-username/celeryviz.git
    ```

3. 🖊️ **Create a branch**  

   Now that you have a copy, it's time to make some magic happen!  
   Create a new branch to work on your feature or bugfix:
    ```bash
    git checkout -b feature-branch
    ```

4. 🔨 **Make your changes**

   Get creative! Add your feature or fix that pesky bug. And remember: no idea is too small we appreciate everything!

5. 🧪 **Test your changes**
  - Ensure redis is running locally on default port `6379` and no other services are using `/0` channel before running tests.

    ```bash
    pytest
    ```

6. 📬 **Send your changes to us**
    ```bash
    git commit -m "Description of your changes"
    git push origin feature-branch
    ```

7. 🔄 **Open a pull request on GitHub**  
   You're almost there! Head over to GitHub and open a pull request (PR) from your branch to the main repository.  

   Tell us about your awesome contribution, and we'll review it ASAP! 🚀  

   Don't forget to give it a nice title and description so we know what it’s all about. 😉


## First Time Contributing? No Worries! 😄
We know getting started can feel a bit overwhelming, we all have been there. But we've got your back! Follow our handy step-by-step guide above, and you'll be contributing like a pro in no time. And if you hit a snag, don't hesitate to ask for help — we're here to support you!


## Code of Conduct 👩‍💻👨‍💻
We want to keep our community as warm and welcoming as a cup of cutting chai on a rainy day! ☕🌧️🍵 Please take a moment to read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to help us maintain a respectful and positive environment for all contributors. ✨

⚠️ **Note:** The Code of Conduct will be strictly enforced. Any violations will be taken seriously, and appropriate action will be taken to maintain a safe and respectful community.


## Development Environment Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/bhavya-tech/celeryviz.git
    ```
2. Build the frontend webapp:
    - The UI webapp is maintained separately in [celeryviz_with_lib](https://github.com/bhavya-tech/celeryviz_with_lib).
    - Run the following command to build the latest version of the standard webapp locally (ensure that [Docker](https://www.docker.com/) is installed):
    ```bash
    docker build --output ./celeryviz/static ./build_ui
    ```
    (It may take some time to build the webapp for the first time.) 

    - For customised builds, the following optional build args can be used:
      - `GITHUB_PAT`: If any of dependency repo is private, add a github personal access token as a build argument.
      - `GIT_REPO`: URL of the repository to build. Defaults to [celeryviz_with_lib](https://github.com/bhavya-tech/celeryviz_with_lib.git)
      - `SOURCE`: The branch of the repository to build. Default is `main`. A particular commit hash can also be used.

    ```bash
    docker build --output ./celeryviz/static --build-arg="GITHUB_PAT=<your github personal access token>" ./build_ui
    ```

3. Install the package in editable mode:
    ```bash
    pip install -e .
    ```


# Thank You! 🙌
You rock! 🤘 Thank you for contributing and helping us make this project even more awesome. We can't wait to see what you'll create!