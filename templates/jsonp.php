<?php
$fname = $_GET['filename'];

echo $_GET['callback']."(".json_encode($fname).")";

?>