# Tutorial Trabalho Prático 1 - Laboratório de Sisop
## Fernanda Rosa e Morgana Weber

#### fernanda.rosa02@edu.pucrs.br
#### morgana.weber@edu.pucrs.br 
<hr>

### <strong>1. Fork do repositorio</strong>
Vá para o repositório <strong>labsisop-buildroot</strong> no perfil da fernandafrosa: https://github.com/fernandafrosa/labsisop-buildroot e faça um fork para o seu perfil.


Depois de fazer o fork, vá para o respositório recém "forkado" em seu usuário. Clique em "Code" e em "Codespaces", selecione "Create codespace". Esse será o ambiente que você usará para o desenvolvimento do tutorial.

<br>
<hr>

### <strong>2. Preparar o Buildroot para compilar para alvo específico</strong>

O comando a seguir deve ser executado para configurar o Buildroot para gerar uma distribuição Linux para emulação com o QEMU:

`$ make qemu_x86_defconfig`

<hr>

### <strong>3. Entre no menu de configurações do Linux:</strong>
Primeiro, você deve instalar o cpio:

`$ sudo apt update`

`$ sudo apt-get install cpio`

`$ make linux-menuconfig`

Habilite o driver Ethernet e1000, como mostrado a seguir (quando abrir o menu depois do ultimo comando terminar de executar)

````
Device Drivers  --->
  	[*] Network device support  --->
  		[*]   Ethernet driver support  ---> 
  		<*>     Intel(R) PRO/1000 Gigabit Ethernet support 
````

Não se esqueça de salvar as alterações antes de sair do menu das configurações.
<hr>

### <strong>4. Compilação:</strong>

`$ make MAKEINFO=false`
<hr>

### <strong>5. Emulando com QEMU:</strong>

`$ sudo apt-get install qemu-system`

Para emular a distribuição compilada execute:

````
sudo qemu-system-i386 --device e1000,netdev=eth0,mac=aa:bb:cc:dd:ee:ff \
    --netdev tap,id=eth0,script=custom-scripts/qemu-ifup \
    --kernel output/images/bzImage \
    --hda output/images/rootfs.ext2 \
    --nographic \
    --append "console=ttyS0 root=/dev/sda"
````
Se pedir buildroot login, o usuário é **root**

Para encerrar o QEMU execute:

`# poweroff`

<hr>

### <strong>6. Configurando a rede:</strong>

Agora, precisamos permitir a comunicação, por rede emulada, entre o sistema operacional guest (emulado pelo QEMU) e a máquina host.

Rode o comando a seguir para dar permissão de execução ao arquivo qemu-ifup, que está dentro da pasta *custom-scripts*

`$ chmod +x custom-scripts/qemu-ifup`

Execute a emulação: 

````
sudo qemu-system-i386 --device e1000,netdev=eth0,mac=aa:bb:cc:dd:ee:ff \
    --netdev tap,id=eth0,script=custom-scripts/qemu-ifup \
    --kernel output/images/bzImage \
    --hda output/images/rootfs.ext2 \
    --nographic \
    --append "console=ttyS0 root=/dev/sda"
````

O usuário é: **root**

Para definir uma senha, use o comando:

`# passwd`

Depois de definir a senha, quando for executar a emulação você deverá digitar o usuário (root) e sua senha definida.

Para sair da emulação, basta digitar:

`$ poweroff`

<hr>

### <strong>7. Testando com PING:</strong>
Precisamos configurar o roteamente de rede no **guest**, para considerar o **host** como seu roteador de primeiro salto. 

Para isso, entre na **máquina guest** e execute:

`$ ifconfig eth0 192.168.1.10 up`

Agora, precisamos, dentro do guest, definir uma rota padrão para o IP do host:

````
$ route add -host <IP-DO-HOST> dev eth0
$ route add default gw <IP-DO-HOST>
````

Para saber o IP do host, você pode utilizar o comando:

`$ ifconfig`

No guest, tente pingar o IP do host:

`$ ping <IP-DO-HOST>`

No host, tente pingar o IP do guest:

`$ ping 192.168.1.10`

Se o comando *ping* não for encontrado, execute na máquina host:

`$ sudo apt-get install iputils-ping`

<hr>

### <strong>8. Tornar configurações no GUEST permanentes:</strong>

Para tornar as configurações no GUEST permanentes, foram criados os arquivos *pre-build.sh* e *S41network-config*, que estão dentro da pasta *custom-scripts*.

Para dar permissão de execução ao arquivo *pre-build.sh*, execute:

`$ chmod +x custom-scripts/pre-build.sh`

Nas configurações do Buildroot já está configurado para executar o script *pre-build.sh* antes da geração da imagem do rootfs.

<hr>



### <strong>9. Adicionando Iperf no target</strong>

Precisamos adicionar suporte ao compilador C++ na toolchain para poder adicionarmos o Iperf.

Na host, execute:

`$ make menuconfig`

Faça as seguintes configurações:

````
Toolchain  --->
  	 [*] Enable C++ support
````

````
Target packages  --->
  	 Networking applications  --->
  		 [*] iperf
````
A modificação na *toolchain* irá exigir a recompilação de toda a distribuição:

`$ make clean`

Como fizemos *make clean*, precisamos assegurar que ainda estamos com as configurações do kernel relacionadas a device drivers configuradas. Portanto, execute:

`$ make linux-menuconfig`

E habilite o driver Ethernet e1000

````
Device Drivers  ---> 
  	[*] Network device support  --->    
  		[*]   Ethernet driver support  ---> 
  		<*>     Intel(R) PRO/1000 Gigabit Ethernet support
````

Salve as configurações e recompile:

`$ make`


<hr>

### <strong>10. Executando testes com Iperf:</strong>
Iperf: opera como um cliente/servidor. 

No diretório *iperf/iperf-2.1.8*, configure e compile o iperf:


````
$ ./configure
$ make
````

O executável estará disponível em *iperf-2.1.8/src/iperf*

**BANDWIDTH:**

Na máquina **target**, execute o comando a seguir:

`$ iperf -s`

Isso fará on iperf aguardar conexões TCP na porta 5001

Na máquina **host**, execute o iperf compilado anteriormente:

`$ iperf/iperf-2.1.8/src/iperf -c 192.168.1.10 -i 1 -t 5`

**JITTER:**
variação do atraso da rede enter 2 hosts

Execute na **target:**

`$ iperf -s -u`

Execute no **host:**

`$ iperf/iperf-2.1.8/src/iperf -c 192.168.1.10 -i 1 -t 5 -u`


<hr>

### <strong>11. Comunicação:</strong>

Primeiro precisamos instalar o pacote *netcat* na distribuição, no menuconfig:

`$ make menuconfig`

````
Target packages  --->
  	[*]   Show packages that are also provided by busybox
  	Networking applications  --->
  		[*] netcat
````

Recompile

`$ make`

Na **target**, usar o programa *nc* para escutar o tráfego TCP na porta 8000:

`$ nc -l -p 8000`

No **host**, use o *nc* para enviar os caracteres digitados no terminal:

`$ nc 192.168.1.10 8000`


<hr>

### <strong>12. Executando o servidor feito em python:</strong>

Na máquina **host**, instale:
E em seguida temos que adicionar o arquivo python a ser rodado para a máquina target.

````
$ sudo apt install ssh
$ sudo apt-get install lynx

$ scp server.py root@192.168.1.10:/

````

Na máquina **target**, depois que o arquivo *server.py* for copiada, entre no arquivo usando `vi server.py` e altere a constante **HOST_NAME** para o IP da máquina target (192.168.1.10).

Então, na máquina **target**, rode o arquivo **server.py** para iniciar o servidor (o arquivo já está pronto, só precisa ser executado)

`$ python server.py`

Para ver as informações da página HTML que acabamos de rodar, na máquina host, execute:

`$ lynx 192.168.1.10`

Pronto! Agora da máquina host você deve conseguir ver a página HTML que rodamos a partir da máquina target!