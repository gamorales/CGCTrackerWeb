<?php

   if (isset($_POST['comando'])) {
       $comando = $_POST['comando'];
       $phone = $_POST['phone'];
       $placa = $_POST['placa'];
       $password = $_POST['password'];
       switch ($comando) {
           case 'lock':
               $datos = ['success'=>1, 'data'=>"Se bloqueó el vehículo $placa - $phone"];
               $comando = 'stop'.$password.';quickstop'.$password;
               break;
           case 'unlock':
               $datos = ['success'=>1, 'data'=>"Se desbloqueó el vehículo $placa - $phone"];
               $comando = 'resume'.$password;
               break;
           case 'speed_on':
               $datos = ['success'=>1, 'data'=>"Se activó la velocidad al vehículo $placa - $phone"];               
               break;
           case 'speed_off':
               $datos = ['success'=>1, 'data'=>"Se desactivó la velocidad al vehículo $placa - $phone"];
               break;
           case 'engine_on':
               $datos = ['success'=>1, 'data'=>"Se activaron las coordenadas del vehículo $placa - $phone"];
               $comando = 'ACC'.$password;
               break;
           case 'engine_off':
               $datos = ['success'=>1, 'data'=>"Se desactivaron las coordenadas del vehículo $placa - $phone"];
               $comando = 'noACC'.$password;
               break;
           case 'movement_on':
               $datos = ['success'=>1, 'data'=>"Se captura movimiento al vehículo $placa - $phone"];
               $comando = 'fix030s030m***n'.$password;
               break;
           case 'movement_off':
               $datos = ['success'=>1, 'data'=>"Ya no se captura movimiento al vehículo $placa - $phone"];
               $comando = 'nofix'.$password;
               break;
           case 'status':
               $datos = ['success'=>1, 'data'=>"Estado del vehículo $placa - $phone"];
               $comando = 'check'.$password;
               break;
           default:
               $datos = ['success'=>0, 'data'=>"No se envió un comando reconocido"];
               break;
        }
       
    } else {
        $datos = ['success'=>0, 'data'=>"No se están enviando los parámetros correctos"];
    }
    
    if ($datos['success']!=0) { 
        
        foreach (explode(";", $comando) as $cmd) {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "https://platform.clickatell.com/messages");
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, "{\"content\": \"".$cmd."\", \"to\": [\"57".$phone."\"]}");
            curl_setopt($ch, CURLOPT_POST, 1);

            $headers = array();
            $headers[] = "Content-Type: application/json";
            $headers[] = "Accept: application/json";
            $headers[] = "Authorization: qNlZit8iQzOWIgMGJz9dUw==";
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

            $result = curl_exec($ch);
            if (curl_errno($ch)) {
                echo 'Error:' . curl_error($ch);
            }
            curl_close ($ch);    
        }

    
        /*curl -i \ 
        -X POST \ 
        -H "Content-Type: application/json" \ 
        -H "Accept: application/json" \ 
        -H "Authorization: qNlZit8iQzOWIgMGJz9dUw==" \ 
        -d '{"content": "Test Message Text", "to": ["573209463858"]}' \ 
        -s https://platform.clickatell.com/messages*/
    }
    echo json_encode($datos);
    
?>