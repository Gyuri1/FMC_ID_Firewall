#
# ACP Rule editor
# 
#
from flask import Flask, render_template, request, url_for, flash, redirect, abort, session
import datetime, time


from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError

from flask import Response

# FMC Credential file
import fmc_config

#acp_rule_update
import acp_rule_update 

# sys  
import sys


app = Flask(__name__)
app.secret_key = "super secret key"

ad_groups = []
selected_ad_groups =[]

# Read AD Groups
@app.route('/', methods=('GET','POST'))
def adgroups():
    global  ad_groups 
    global  selected_ad_groups

    if request.method == 'GET':

        ad_groups=[]
        ad_filter="(memberOf="+fmc_config.ad_base_dn+")"

        ad_server = Server(host=fmc_config.ad_host,port=fmc_config.ad_port,get_info = ALL)
        ad_conn   = Connection(ad_server, user=fmc_config.ad_admin, password= fmc_config.ad_password, auto_bind= True)

        ad_conn.search(search_base=fmc_config.ad_base_dn,
                    search_filter='(objectClass=group)',
                    attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES], size_limit=0)
    
        for e in sorted(ad_conn.entries):
            ad_groups.append(e.name)

        ad_conn.unbind()

    elif request.method == 'POST':
        if  request.form.get('submit_button') == 'select':
            selected_ad_groups  = request.form.getlist('ad_groups')
            print("Selected AD groups:", selected_ad_groups)
        elif request.form.get('deploy_button') == 'deploy':    
            print("Deploy:")
            print("Selected AD groups:", selected_ad_groups)
            acp_rule_update.deploy(selected_ad_groups, "deploy" )
        elif request.form.get('reset_button') == 'reset':    
            print("Reset:")
            selected_ad_groups =[]
            print("Selected AD groups:", selected_ad_groups)
            acp_rule_update.deploy(selected_ad_groups, "reset" )
    return render_template('index.html', ad_groups=ad_groups, selected_ad_groups=selected_ad_groups )


# Settings
@app.route('/settings/', methods=('GET','POST'))
def settings():
   
    if request.method == 'POST':
        fmc_config.host = request.form['fmchost'] 
        if not fmc_config.host:
            flash('FMC host is required!')

        fmc_config.admin = request.form['fmcadmin'] 
        if not fmc_config.admin:
            flash('FMC admin is required!') 

        fmc_config.password = request.form['fmcpassword'] 
        if not fmc_config.password:
            flash('FMC password is required!') 

        fmc_config.acp_policy = request.form['acp_policy'] 
        if not fmc_config.acp_policy:
            flash('ACP policy name is required!')           

        fmc_config.ace_rule_name = request.form['ace_rule_name'] 
        if not fmc_config.ace_rule_name:
            flash('IPS rule number is required!')  
          
        # AD parameters    
        fmc_config.ad_host = request.form['ad_host'] 
        if not fmc_config.ad_host:
            flash('AD host is required!')

        fmc_config.ad_admin = request.form['ad_admin'] 
        if not fmc_config.ad_admin:
            flash('FMC admin is required!') 

        fmc_config.ad_password = request.form['ad_password'] 
        if not fmc_config.ad_password:
            flash('AD password is required!')    

        fmc_config.ad_port = int(request.form['ad_port']) 
        if not fmc_config.ad_port:
            flash('AD port is required!') 

        fmc_config.ad_base_dn = request.form['ad_base_dn'] 
        if not fmc_config.ad_base_dn:
            flash('AD base DN is required!')     

          
    return render_template('settings.html', fmchost=fmc_config.host, \
    fmcadmin=fmc_config.admin, fmcpassword=fmc_config.password, \
    acp_policy=fmc_config.acp_policy, ace_rule_name= fmc_config.ace_rule_name,  \
    ad_host= fmc_config.ad_host, ad_admin= fmc_config.ad_admin, \
    ad_password= fmc_config.ad_password, ad_port= fmc_config.ad_port, \
    ad_base_dn= fmc_config.ad_base_dn) 


if __name__ == "__main__":

    app.debug = True
    app.run()
