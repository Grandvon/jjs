<?php
$vote = $_REQUEST['vote'];

//get content of textfile
$filename = "poll_result.txt";
$content = file($filename);

//put content in array
$array = explode("||", $content[0]);
$ps4 = $array[0];
$xboxone = $array[1];

if ($vote == 0) {
  $ps4 = $ps4 + 1;
}
if ($vote == 1) {
  $xboxone = $xboxone + 1;
}

//insert votes to txt file
$insertvote = $ps4."||".$xboxone;
$fp = fopen($filename,"w");
fputs($fp,$insertvote);
fclose($fp);
?>

<h2>Result:</h2>
<table>
<tr>
<td>PS4:</td>
<td>
<img src="poll.gif"
width='<?php echo(100*round($ps4/($xboxone+$ps4),2)); ?>'
height='20'>
<?php echo(100*round($ps4/($xboxone+$ps4),2)); ?>%
</td>
</tr>
<tr>
<td>Xbox One:</td>
<td>
<img src="poll.gif"
width='<?php echo(100*round($xboxone/($xboxone+$ps4),2)); ?>'
height='20'>
<?php echo(100*round($xboxone/($xboxone+$ps4),2)); ?>%
</td>
</tr>
</table>
