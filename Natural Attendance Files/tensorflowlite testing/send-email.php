<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

require 'PHPMailer/src/Exception.php';
require 'PHPMailer/src/PHPMailer.php';
require 'PHPMailer/src/SMTP.php';

//Create an instance; passing `true` enables exceptions
$mail = new PHPMailer(true);

// Get the POST data from the Ajax request
$to = $_POST['email'];

//die($to);
$subject = $_POST['subject'];
$message = $_POST['message'];
//die($message);
$mail->SMTPDebug= SMTP::DEBUG_SERVER;
$mail->isSMTP();
$mail->Host = 'smtp.yandex.com';
$mail->SMTPAuth = true;
$mail->Username = 'ijngc@perpetualinnovation.net';
$mail->Password = '#perpetual';
$mail->SMTPSecure = 'tls';
$mail->Port = 587;
$mail->setFrom('info@perpetualinnovation.net', 'System Notification');
$mail->addAddress($to);
$mail->Subject = $subject;
$mail->Body = $message;

if (!$mail->send()) {
    echo 'Error: ' . $mail->ErrorInfo;
} else {
    echo 'Email sent successfully';
}
?>
