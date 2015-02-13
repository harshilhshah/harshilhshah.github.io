<?php

require_once("cron.php");
$interval=60; //minutes
    set_time_limit(0); 

    while (true)
{
$now=time();
giantMethod();
sleep($interval*60-(time()-$now));
}
