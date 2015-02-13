<?php
    /* Send an SMS using Twilio. You can run this file 3 different ways:
     *
     * - Save it as sendnotifications.php and at the command line, run 
     *        php sendnotifications.php
     *
     * - Upload it to a web host and load mywebhost.com/sendnotifications.php 
     *   in a web browser.
     */
 
    require "Services/Twilio.php";
    require_once("secrets.php");
 
 function giantMethod(){
    $AccountSid = getSid();
    $AuthToken = getToken();
    $client = new Services_Twilio($AccountSid, $AuthToken);
    	    
    $name = getName();
    $number = getNumber();

    $BASE_URL = "https://query.yahooapis.com/v1/public/yql";  
    $yql_query = "select * from html where url='https://secure-gorge-6111.herokuapp.com'";  
    $yql_query_url = $BASE_URL . "?q=" . urlencode($yql_query) . "&format=json"; 

    $session = curl_init($yql_query_url);  
    curl_setopt($session, CURLOPT_RETURNTRANSFER,true);  
    $json = curl_exec($session);  
    // Convert JSON to PHP object   
    $phpObj =  json_decode($json);  
    echo $phpObj->query->results->body->pre->content;

   $sms= $client->account->messages->sendMessage(
             "908-304-9250", 
 	     "+1$number",
            "Hey $name!"
    );

    echo "Sent message to $name \n";
}