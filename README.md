# SDUI

SDUI (Secure Device to Upload Information) is a Python and Web project for assure the integrity of the files and network on Foxconn PCE Paragon Solutions avoiding the intrusion of malwares, supported on Microsoft SharePoint to upload all files recieved. This project only will work on Raspberry with Raspbian OS. 


## Preparation

Once upon you downloaded the "imageSDUI.iso" from this repository, you will need to upload it into a MicroSD at least 64 GB. This ISO image contains a workly version of SDUI. To assure all files are updated please execute the next commands. (For this, you MUST have an internet connection)

```bash
cd sdui/
git pull https://github.com/mariolopez2/sdui
```

## Configuration

To complete setup, you have to run the next command. (this script will try to reconfigure all necessary)

*NOTE*: For this step you need to have what IP Address you will assign and all network details provides by Network Engineer. 

```bash
sudo python3 setup.py 
```

Once upon you finished with this configuration, it is necessary to start with RClone configuration, for this please make sure to read "RClone_configuration.pdf" 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)icense.com/licenses/mit/)
