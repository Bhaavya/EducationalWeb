## EducationalWeb

### Table of Contents
- [Project Setup Instructions](#instructions)
    - [MacOS](#instructions-macos)
    - [Windows](#instructions-win)
- [Additional Notes](#additional-notes)
- [Pre-Deployment Test Checklist](#test-checklist)
- [Releases](#releases)

### Setup Instructions <a name="instructions">

#### MacOS <a name="instructions-macos">

Step 0: Download the project in a local directory/folder. 

Step 1: Create a virtual environment in the project and then activate it

    a. Open the directory where the project is stored in your terminal.
    
    b. Run: pip install virtualenv  
            Installs the compnonents needed to create a virtual environment in your current directory.
    
    c. Run:  virtualenv env
            Creates a virtual environment with the name env in your current directory. It can be actually named anything that you like, some common names are venv and env.
    
    d. Run: source env/bin/activate
            It changes the current environment from base to env. After this step you should see that the word env or your environment's name is located inside brackets. That shows that you are now using the env environment.
    
    e. Run: deactivate
            This command deactivates the current virtual environment env and should go to base virtual environment. The next steps (Step 3) should be followed in the base virtual environment until the steps ask to activate the env virtual environment.
    

Step 2: Now our next step is to turn on the Redis server:
    a. Run: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            This command downloads components needed to succesfully install redis.
            
    b. TROUBLESHOOT:
    
    c. Run: brew install redis
            This step installed all the components to activate the redis server.
        
    d. Run: redis-server --port 8097 
            This step turns on the redis-server --port for this project because the localhost port # is 8097.
    
    e.  Activate the env virtual environment again. Run: redis-cli -p 8097 ping
            After running the above command 
            
    
Step 3: Install Flask SSE, gunicorn, and gevent.

    a. Run: pyvenv sse
            This command downloads the flask sse components in the project directory.
    
    b. Run: pip install flask-sse gunicorn gevent
            This command downloads the gunicorn and gevent components in the project directory.
            
    c. Run: pip install --upgrade gensim
            This command installs the genism components in your project directory.
            
    d. Run: pip install elasticsearch==7.15.2
            This command installs the elasticsearch of version 7.15.2 (Version is important for the search engine to work) components in your project directory.
  
    
Step 4: Make sure you are in the project's directory and the env virtual environment is activated before running the commands below.

    a. Run: npm install
            This command installs the node modules directory in the local machine, which will be used to succesfully install the gulp components.
    
    b. Run: npm install --global gulp-cli
            This command installs the gulp components in the local machine.     
            
    
    b. Run: cd pdf.js/build/generic/web
            This command makes the terminal to activate this web directory.
    
    c. Run: gulp server
            This command then Activates the gulp server in the web directory.
     
    d. TROUBLESHOOT: If you have trouble running gulp server then run: npm update
        This step basically upgrades the gulp compnonents incase they weren't downloaded to its full potential.
        

Step 5: Run the program in the local machine

    a.Run: gunicorn edwb_app_intro:app --worker-class gevent --bind 127.0.0.1:8097
    
    b. TROUBLESHOOT: If the machine lags and runs forever then run: gunicorn edwb_app_intro:app --worker-class gevent --bind 127.0.0.1:8097 --timeout 600
        This allow the local host to load everything in a limited time frame.

##### Additional components for successfully uploading the project in your computer:
   ###### Downloading the following folders from Google Drive and place them in your project's directory:
    1. static
    2. pdf.js
    3. MACOSX
    
    * Please note that some of the folders are large and may need some time to download.

#### Windows <a name="instructions-win">

We will go over how the installation steps for Windows differ from those of Apple.

Step 1: Download the project in a local directory/folder (same as above).

Step 2: Install gulp and redis

    a. Run: npm intall --save npm-git-install
        a.1. Verify successful installation by running: gulp --version
        
    b. Run: 
        b.1. curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
        b.2. echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
        b.3. sudo apt-get update
        b.4. sudo apt-get install redis
        
    c. Start redis server by running: sudo service redis-server start
    
    d. Test that redis server is running by connecting with cli:
        d.1. redis-cli
             127.0.0.1:8097> ping
             PONG
 
 Step 3: Install Flask SSE, gunicorn, and gevent (same as above)
 
    a. Run: pyvenv sse
    
    b. Run: pip install flask-sse gunicorn gevent

Step 4: Install wsl and ubuntu:

    a. Run: sudo apt install net-tools
    
    b. Run: sudo apt install wsl
    
    c. Run: wsl --install -d Ubuntu

Running EduWeb on local machine:

Step 1:

    a. In a new Ubuntu terminal, cd into pdf.js/build/generic/web
    
    b. Run the command: gulp server
        b.1. gulp ensures that the lecture slides appear on the website
    
Step 2:

    1. In a separate Ubuntu terminal, run: sudo service redis-server start 
    
    2. In the same Ubuntu terminal, cd into web directory (usually a path beginning with /mnt/c/Users). Then run: redis-server --port 8097
        2.a. This starts up redis

Step 3: 

    a. In a separate Ubuntu terminal, cd into wherever you saved the web directory (usually a path beginning with /mnt/c/Users)

    b. Kill redis (ctrl c in the Ubuntu terminal where you started redis)
    
    c. Run the following command in the separate Ubuntu terminal: gunicorn edwb_app_intro:app --worker-class gevent --bind 127.0.0.1:8097
    If the program times out, run: gunicorn edwb_app_intro:app --worker-class gevent --bind 127.0.0.1:8097 --timeout 600
    This means the program will run for 600 extra seconds before timing out. Feel free to increase this number to allow for more time.
    
Step 4:

    a. To allow for functionality of search bar(s), connect to vpn.illinois.edu


### Note on data/model-related files <a name="additional-notes">

Since GitHub has file size limits, we cannot upload some of the data and model-related files to GitHub. They must be uploaded separately (for instance, via Google Drive). You may have to download these files separately (please contact one of the owners for more details).

### Test Checklist <a name="test-checklist">

Please use this checklist before deployment to check for any bugs in the app/code
Update this checklist before every release.

Menu
- [ ] Navigate to the course first lecture by clicking on the course from Courses Dropdown
- [ ] Search for the course in the Courses Dropdown
- [ ] Navigate to the lecture first slide by clicking on the lecture from Lectures Dropdown
- [ ] Search for the lecture in the Lectures Dropdown

Recently Visited Slides
- [ ] Clicking on a recently visited slide from dropdown updates the slide in the Main body 
 
Scrolling Slide Thumbnail
- [ ] Clicking on thumbnail of a slide updates the slide in main body and highlights the slide with a yellow border

Main Slide
- [ ] Download button downloads pdf for lecture
- [ ] Download button downloads all lectures zip
- [ ] Select text and click on explain button, should show explanation or no explanation found
- [ ] Next button and keyboard "**>**" arrow goes to next slide in the pdf
- [ ] Prev button and keyboard "**<**" arrow goes to prev slide in the pdf
- [ ] Next button disabled when reaching end of pdf
- [ ] Prev button disable when reaching start of pdf

Tooltips

- [ ] On Hover search icon - show tooltip for search
- [ ] On Hover search filter - show tooltip
- [ ] On Hover download slides button - show tooltip
- [ ] On Hover explain button - show tooltip
- [ ] On Hover next/prev button - show tooltip

Related Slides Sidebar
- [ ] Related slide links show on the sidebar for each slide 
- [ ] Hovering on related slides, show the slide thumbnail
- [ ] Clicking on a slide link from here updates the pdf in the Main Slide

Search Bar 
- [ ] Can search and filter by course, with/without spaces
- [ ] Keyword search and see the list of results 

Feedback and Report Bug Buttons
- [ ] Clicking Feedback displays the feedback form
- [ ] Clicking Report Bug displays the report bug form 

Logging 

Schema used 
```
HOST,KEYWORD (in case of search),TIMESTAMP,ACTION_TYPE 
```
- [ ] Logs with above schema when using Search functionality (ACTION_TYPE: search)
- [ ] Logs with above schema when using the Explain functionality (ACTION_TYPE: explain)
- [ ] Logs with above schema when changing to new slides (ACTION_TYPE: open/close)
- [ ] Logs with above schema when changing to slides using Next/Prev button (ACTION_TYPE: next/prev)
- [ ] Logs with above schema when clicking on related slides from sidebar (ACTION_TYPE: related_slide_<idx>)
- [ ] Logs with above schema when hiding/unhiding slides (ACTION_TYPE: hide/unhide)

### Releases <a name="releases">

**Release v2** 

Deployed on 11/22/22

Changes made:
- Next/Prev- Next and Prev button style change and disables when reaches the start or end of slides
Above the slide utility buttons 
- Changed button/icon styles to explain, download text book, lecture pdfs
Explanation implementation 
- Updated the implementation of explain function, it is simplified and covers edge case scenarios. Added asynchronous response for a user explain request , updated from sse event where the server published the same response to all clients.
Fixed TextLayer Overlapping
- TextLayer is the layer of text that is parsed from each pdf slide and is an html element that is invisible but selectable. 
- Fixed Scrolling issue with Sidebar thumbnails
- Added Search box in courses and lectures dropdown
- Added course filter in Search bar
- Decreased latency for slide load in the thumbnails when hovering on slide links 

**Release v3** 

Changes

Major 
- Refactored code and cleaned directories and files not used
- Added and updated logging code for related slides, search, explain, next/prev functionalities

Minor 
- Added arrow keys for to navigate next/prev slides 
- Added report bug button and embedded form
- Added tooltips 
- Added gitignore file 
- Removed config.py file 


