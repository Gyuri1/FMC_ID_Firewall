#
# FMC ACP rule updater
# 

# import required dependencies
import json


# FMC Credential file
import fmc_config

# FMC Class
from fmc_class import fmc


def deploy(ad_list, action):

    target_domain = "Global"
 
    print("Get FMC token:")

    # Set variables for execution.
    # Make sure your credentials are correct.
    device   = fmc_config.host
    username = fmc_config.admin
    password = fmc_config.password

    # Initialize a new api object
    print("FMC authentication for this FMC:", device)
    api = fmc(host = device, username=username, password=password)
    api.tokenGeneration(target_domain)
    print("Token received.")
    for domain in api.domains["domains"]:
        print("Domain name:",domain["name"],"UUID:",domain["uuid"] )

    
    print("Reading ACP policy ID:")
    result=api.get_accesspolicies()
    #json_formatted_str = json.dumps(result, indent=2)
    acp_policies = result["items"]
    for i in acp_policies:
        if (i["name"] == fmc_config.acp_policy):
            acp_policy_id = i["id"]

    print("ACP name:", fmc_config.acp_policy, "acp_policy_id:",acp_policy_id)
   
    print("Reading rule:",fmc_config.ace_rule_name)
    result=api.get_acp_rules(acp_policy_id)
    ace_rules = result["items"]
    for i in ace_rules:
        if (i["name"] == fmc_config.ace_rule_name):
            ace_rule_id = i["id"]

    print("Rule ID:",ace_rule_id)

    rule=api.get_acp_rule(acp_policy_id, ace_rule_id)
    json_formatted_str = json.dumps(rule, indent=2)
    #print("Rule:", json_formatted_str)



    #Get Realms
    realms=api.get_realms()
    json_formatted_str = json.dumps(realms, indent=2)
    #print("Realms:",json_formatted_str)
    domains = realms["items"]

    target_domain = fmc_config.ad_base_dn.replace(',', '.').replace('DC=', '').replace('dc=', '')

    print("Target Domain:", target_domain)

    for i in domains:
        if (i["name"] == target_domain):
            target_domain_id = i["id"]
    print("Target domain id:", target_domain_id)
    

    #result=api.get_realm(target_domain_id)
    #json_formatted_str = json.dumps(result, indent=2)
    #print("Realm content:",json_formatted_str)

    #target_ad_id=result['version']
    #print("AD ID :",target_ad_id)

    #result=api.get_groups_from_realm(target_ad_id)
    #result=api.get_groups_from_realm('2')   

    fmc_groups = api.get_realmusergroups()
    json_formatted_str = json.dumps(fmc_groups, indent=2)
    #print("Groups:",json_formatted_str)

    target_groups=[]
    for j in ad_list:
        for i in fmc_groups["items"]:
            if (j == i["name"]):
                target_groups.append( {'name':i['name'], 'id': i['id'], 'type': 'RealmUserGroup',\
                   "realm": { "id": target_domain_id, \
                   "type": "Realm", "name": target_domain}})
    print("Target Groups:", target_groups)



    if action =="deploy":
        rule["enabled"] = True
    elif action =="reset":
        rule["enabled"] = False  

       
    rule.pop('metadata', None)
    rule.pop('links', None)

    if target_groups:
        print("NEW Target Groups:")
        rule["users"] = { "objects": target_groups}

        #json_formatted_str = json.dumps(rule, indent=2)
        #print("NEW Rule:", json_formatted_str)

    result=api.put_acp_rule(acp_policy_id, ace_rule_id, data=rule)
    json_formatted_str = json.dumps(result, indent=2)
    #print("PUT Output:",json_formatted_str)
   
    # Deployment
    print("GET deployabledevices ")
    result=api.get_deployabledevices()
    json_formatted_str = json.dumps(result, indent=2)
    #print(json_formatted_str)

    if 'items' in result: 
      deploy_version=result["items"][0]["version"]
      device_name=result["items"][0]["name"]
      #print("GET devices ")
      result=api.get_devices()
      json_formatted_str = json.dumps(result, indent=2)
      #print(json_formatted_str)
      for i in result['items']:
      	if device_name == i["name"]:
      		device_uuid = i["id"]	
    else:
      print("ERROR: no device")
      exit()

    print("device UUID", device_uuid)

    deploy_post={
      "type": "DeploymentRequest",
      "version": deploy_version,
      "forceDeploy": False,
      "ignoreWarning": True,
       "deviceList": [ device_uuid ],
      "deploymentNote": "AD Group based ACP deployment"
    }

    print("Deployement: started ... ")
    result=api.deploymentrequests(deploy_post)
    json_formatted_str = json.dumps(result, indent=2)
    #print(json_formatted_str)
    return True
    
