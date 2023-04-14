# Tutorial Trabalho Prático 1 - Laboratório de Sisop
## Fernanda Rosa e Morgana Weber

#### fernanda.rosa02@edu.pucrs.br
#### morgana.weber@edu.pucrs.br 
<hr>

### <strong>1. Iniciando a máquina emulada </strong>
No terminal, execute o seguinte comenado para incializar a máquina emulada: 
````
sudo qemu-system-i386 --device e1000,netdev=eth0,mac=aa:bb:cc:dd:ee:ff \
    --netdev tap,id=eth0,script=custom-scripts/qemu-ifup \
    --kernel output/images/bzImage \
    --hda output/images/rootfs.ext2 \
    --nographic \
    --append "console=ttyS0 root=/dev/sda"
````
### <strong>2. Abrindo um novo terminal </strong>
Abra um novo terminal para executar os comandos referentes ao **host**.

### <strong>3. Executando o servidor feito em Python:</strong>

Na máquina **host**, instale o Python caso ele não esteja instalado : 
````
 $ sudo apt-get install python3
````
E em seguida temos que enviar o arquivo python a ser rodado para a máquina **target**.
````
$ sudo apt install ssh
$ sudo apt-get install lynx

$ scp server.py root@192.168.1.10:/

````

Na máquina **target**, depois que o arquivo *server.py* for copiada, entre no arquivo usando `vi server.py` e altere a constante **HOST_NAME** para o IP da máquina target (192.168.1.10).

Então, na máquina **target**, rode o arquivo **server.py** para iniciar o servidor (o arquivo já está pronto, só precisa ser executado)

````
$cd .. 
$ python server.py
```` 
Com isso, você verá a seguinte mensagem no terminal, dizendo que o server foi incializado no endereço x que será o endereço acessado na máquina **host**: 
![image](https://user-images.githubusercontent.com/77460481/232125557-ca25c81e-8b33-436b-9ed1-28bd170e11f4.png)


Para ver as informações da página HTML que está no servidor que acabamos de rodar, na máquina **host**, execute:

`$  lynx  http://192.168.1.10:8080`

Pronto! Agora da máquina **host** você deve conseguir ver a página HTML que rodamos a partir da máquina **target**, porém no navegador para terminal, então você deverá estar enxergando algo semelhante à imagem: 
![image](https://user-images.githubusercontent.com/77460481/232125793-90e50786-dc06-4693-adc1-3a57d9e47551.png)

Enquanto isso, você poderá acompanhar a requisição feita pelo **host** no terminal da **target**:
![image](https://user-images.githubusercontent.com/77460481/232125950-c8a448f1-760b-440b-a349-45d49e91244b.png)
