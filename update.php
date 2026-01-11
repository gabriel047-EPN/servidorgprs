<?php
$mq2  = $_POST['mq2'] ?? 'NA';
$door = $_POST['door'] ?? 'NA';

$data = [
  "mq2" => $mq2,
  "door" => $door,
  "time" => date("Y-m-d H:i:s")
];

file_put_contents("data.json", json_encode($data));
echo "OK";
?>
