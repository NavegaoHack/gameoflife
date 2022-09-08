echo hello
which python3
if  [ $? -eq 0 ]
then
    echo "python3 está instalado"

    if [[ -d venv ]]
    then
        echo "el entorno virtual está en la carpeta"
    else
        echo "no hay entorno virtual, creando uno entorno..."
        
        python3 -m pip --version
        if [ $? -eq 1 ]
        then
            echo "instalando pip"
            echo "Se instalarán los paquetes pip, setuptools, y wheel"
            sudo python3 master/get-pip.py --prefix=/usr/local/
            python3 -m pip install --upgrade pip setuptools wheel
            python3 -m pip --version
            echo "pip ha sido instalado correctamente"
        else
            echo "pip ya está instalado"
        fi
        echo "creando..."
        python3 -m venv venv
        source venv/bin/activate
        echo "descargando módulos"
        python -m pip install pygame
        python -m pip install numpy
        echo "lista de paquetes del entorno virtual"
        python -m pip list
        echo "entorno virtual creado y configurado"
        deactivate
    fi

    echo ""
    echo "---------INICIANDO-----------"
    echo ""
    source venv/bin/activate
    python master/game.py
    deactivate
    echo ""
    echo "---------FINALIZADO----------"
    echo ""

else
    echo "python3 no está instalado en el sistema, se le sugiere instalarlo desde su página oficial"
fi