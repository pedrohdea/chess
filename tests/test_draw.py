import cv2

# Abre o vídeo (pode ser um arquivo ou webcam com cv2.VideoCapture(0))
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break  # vídeo acabou

    # Aqui você pode desenhar no frame
    cv2.putText(frame, "Teste", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Atualiza a mesma janela com o novo frame
    cv2.imshow("Video", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
