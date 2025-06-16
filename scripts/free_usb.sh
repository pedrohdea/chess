# 1. Adicione seu usuário ao grupo dialout (em distribuições baseadas em Debian/Ubuntu):
sudo usermod -a -G dialout $USER

# 2. Verifique as permissões atuais da porta:
ls -l /dev/ttyACM0

# 3. Permissão temporária (não recomendado para uso permanente):
sudo chmod 666 /dev/ttyACM0
