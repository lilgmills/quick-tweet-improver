# OpenAI API Tweet improver - modified Python example app

This is an example tweet improver app modifying the OpenAI API [quickstart tutorial](https://beta.openai.com/docs/quickstart). It uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. Check out the tutorial or follow the instructions below to get set up.

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```
   bash
   $ cd quick-tweet-improver
   ```
   
   ```
   Command Prompt
   > cd quick-tweet-improver
   ```

4. Create a new virtual environment:

   ```
   bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```
   
   ```
   Command Prompt
   > python -m venv venv
   > . venv/Scripts/activate
   ```

5. Install the requirements:

   ```
   bash
   $ pip install -r requirements.txt
   ```
   
   ```
   Command Prompt
   > pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```
   bash
   $ cp .env.example .env
   ```
   
   ```
   Command Prompt
   > copy .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

8. Run the app:

   ```
   bash
   $ flask run
   ```
   
	```
	Command Prompt
   > flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000).

For the full context behind the example app this modifies, check out the OpenAI [quickstart tutorial](https://beta.openai.com/docs/quickstart).
