## EducationalWeb

### Here are the instructions for getting started with the proejct:

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
    a. First make sure you have homebrew installed 
    
    b. Run: brew install redis
        This step installed all the components to activate the redis server.
        
    c. Run: redis-server --port 8097 
            This step turns on the redis-server --port for this project because the localhost port # is 8097.
    
    d.  Activate the env virtual environment again. Run: redis-cli -p 8097 ping
            After running the above command
    
Step 2: Install Flask SSE, gunicorn, and gevent.
    

Step 4: In your current directory and 

    a. npm install --global gulp-cli
    
    b. cd pdf.js/build/generic/web
        The
    
    c. Run: gulp server
            Activates the gulp server.
    
    d. TROUBLESHOOTING: If you have trouble running gulp server then run: npm update
        This step basically upgrades the gulp compnonents incase they weren't downloaded to its full potential.
        

Finally Run: gunicorn edwb_app_intro:app --worker-class gevent --bind 127.0.0.1:8097



