# RaspberryPi-Traffic-Lights
Using traffic lights on Raspberry Pi GPIO to create a tactile monitoring system for salespeople and other staff.

I wanted to monitor how salespeople were performing in a way that was easier than to check a sales leaderboard. I wanted to see from looking at them, how they were doing.

This simple script allows you to place a Raspberry Pi on the desk of a salesperson (or whichever type of staff you wish to monitor) and show red, amber or green lights, depending on their KPIs and how they are currently doing.

## How it works
An instructions file should be written to and available on the web. This allows the main script (sales.py) to load the URL and for each Raspberry Pi to read its own data.

The instructions file is very simple. For each Raspberry Pi, create a line with the following parameters:
* Mac Address
* Current KPI number (eg how many calls they have made today)
* Milestone of KPI (eg half the number of calls required)
* Target number (of calls, for example)

A typical instructions file looks like:

    0xb827eb8b9e84L:11:20:40:
    0x9e30356476abL:32:20:40:
    0xfaafe1c40752:41L:20:40:
This shows the instructions for 3 different Raspberry Pi's running the main script. Each computer will read the line that corresponds with its own Mac Address. Broken down, this is what each field of a line represents:

* `62:3a:da:b7` - mac address
* `33` - number of calls actually made today by person with this Raspberry Pi on their desk
* `20` - number of calls to be made to make amber light appear
  * - if this target hasn't been reached then light will flash red 
* `40` - the target number of calls to be made to make green light appear

In the case of the line above, the amber light of this salesperson's Traffic Light would be shown because calls (`33`) are greater than `20` but less than the full target of `40`.

To create the data for the instructions file, you can manually input it into a text file and keep updating it using ftp etc, or extract information from your own phone system and uploading periodically, if you run a sales team.

## Main Script (sales.py)
This script should be placed in your home directory on your Raspberry Pi (`/home/pi`). You only need to change one variable and that is the `target_url`, which is where you will place your instructions.

It is recommended that you run the script when the Raspberry Pi boots, and this can be done using the `@reboot` function in crontab. An example entry could be:

`@reboot sudo python /home/pi/sales.py &`

## Things to note
You should find your 


