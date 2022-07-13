## EducationalWeb

### Here are the instructions for getting started with the project:

#### Apple/iOS

Step 0: Download the project in a local directory/folder. 

Step 1: Create a virtual machine in the project and then activate that virtual machine.

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
            
    
Step 2: Install Flask SSE, gunicorn, and gevent.
    a. Run: pyvenv sse
            This command downloads the flask sse components in the project directory.
    
    b. Run: pip install flask-sse gunicorn gevent
            This command downloads the gunicorn and gevent components in the project directory.
    

Step 4: Make sure you are in this project's directory and env virtual environment is activated before running the commands below.

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

#### Windows

We will go over how the installation steps for Windows differ from those of Apple.

Step 0: Download the project in a local directory/folder (same as above).

Step 1: 

Step 5: In the Ubuntu terminal, run the program on the local machine
    a) cd into /mnt/c/Users
    b) From there, cd into wherever you saved the web directory
    c) Run the following command: gunicorn edwb_app_intro:app --worker-class gevent --bind 127.0.0.1:8097
    If the program times out, run: gunicorn edwb_app_intro:app --worker-class gevent --bind 127.0.0.1:8097 --timeout 600
    This means the program will run for 600 extra seconds before timing out. Feel free to increase this number to allow for more time

### Here are instructions for data/model-related files:

Since GitHub has file size limits, we cannot upload some of the data and model-related files to GitHub. They must be uploaded separately (for instance, via Google Drive). We go over where to download these files from and which directory to place them in. 
