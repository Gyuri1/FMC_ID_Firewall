# FMC_ID_Firewall


This tool can demonstrate Cisco FMC Access Control Policy (ACP) ID based firewall using REST API. 


# How to install:

  Copy all of the files from current repository into a working directory.    
  
  Install the necessary python libraries:  
  `pip install requests`  
  `pip install flask`  

# How to use:


You can run the flask application with this command:

    `python app.py`


Please visit http://127.0.0.1:5000/ 

![Flask GUI](/flask_gui.jpg?raw=true "Flask GUI")

`Settings` menu: you can configure the FMC and AD parameters.  
`AD Group Based Policy` menu : You can select the necessary AD groups.  


`Select Groups` : You can enter the necessary AD groups into the system.  
`Deploy`: New policy will be deployed.  
`Reset`: The policy will be modified with disabled rule.  


# WARNING: 

- Please review the NEW policy before deploying it!  
- Use it at your own risk! THIS IS DEMO CODE - NO WARRANTY OR SUPPORT IS IMPLIED OR PROVIDED!  
- PRs are welcome!   
- It was tested with FMC 7.3 versions as well, but older releases were not tested.  
