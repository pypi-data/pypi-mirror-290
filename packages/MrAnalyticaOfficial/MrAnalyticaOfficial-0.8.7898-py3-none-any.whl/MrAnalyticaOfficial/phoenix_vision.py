import cv2
import os
import numpy as np
import time
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint
import os
import sys
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class PhoenixVision:
    def __init__(self, training_data_dir='training_data', model_path='face_recognition_model.keras'):
        self.training_data_dir = training_data_dir
        self.model_path = os.path.join("C:\\Users\\aluno\\Desktop\\m", model_path)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.model = None
        self.labels = {}
        self.training_duration = 60
        self.image_paths = []

        if os.path.exists(self.model_path):
            print(f"Carregando modelo de {self.model_path}")
            self.model = load_model(self.model_path)
        else:
            print("Modelo não encontrado. O treinamento será necessário.")
        if os.path.exists('labels.txt'):
            with open('labels.txt', 'r') as f:
                for line in f:
                    name, id_ = line.strip().split(':')
                    self.labels[name] = int(id_)

        # Cria o modelo se ele não existir ou se for None
        if not os.path.exists(self.model_path) or self.model is None:
            print("Criando novo modelo...")
            self.model = self.create_model()
    
    def create_model(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 1)))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dense(len(self.labels), activation='softmax'))

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def load_training_data(self):
        if not os.path.exists(self.training_data_dir):
            os.makedirs(self.training_data_dir)

        image_paths = []
        for root, dirs, files in os.walk(self.training_data_dir):
            for file in files:
                if file.endswith('.png'):
                    image_paths.append(os.path.join(root, file))

        print("Imagens encontradas:", len(image_paths))

        faces = []
        ids = []

        for image_path in image_paths:
            face_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            faces.append(face_img)

            label = os.path.basename(os.path.dirname(image_path))
            if label in self.labels:
                id_ = self.labels[label]
            else:
                id_ = len(self.labels)
                self.labels[label] = id_
            ids.append(id_)

        print("Número de faces:", len(faces))
        print("Número de IDs:", len(ids))
        print("Labels:", self.labels)

        self.image_paths = image_paths

    def train_model(self):
        features = []
        labels = []

        for image_path in self.image_paths:
            face_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            face_img = face_img / 255.0
            features.append(face_img.reshape(200, 200, 1))

            label = os.path.basename(os.path.dirname(image_path))
            label_id = self.labels[label]
            labels.append(label_id)

        features = np.array(features)
        labels = np.array(labels)

        X_train, X_val, y_train, y_val = train_test_split(features, labels, test_size=0.2, random_state=42)

        checkpoint = ModelCheckpoint(filepath=self.model_path, verbose=1)

        print("Iniciando o treinamento...")
        try:
            print(f"Caminho do modelo: {self.model_path}")
            history = self.model.fit(
                X_train, 
                y_train, 
                epochs=10, 
                validation_data=(X_val, y_val), 
                callbacks=[checkpoint]
            )
            print(f"Histórico do treinamento: {history.history}")
            print("Treinamento concluído!")

        except Exception as e:
            print(f"Erro durante o treinamento: {e}")

        with open('labels.txt', 'w') as f:
            for name, id_ in self.labels.items():
                f.write(f'{name}:{id_}\n')

    def TimeRecognize(self, minutes):
        self.training_duration = minutes * 60

    def set_cam_ip(self, ip_address):
        """
        Configura a captura de vídeo para usar uma câmera IP.

        Args:
            ip_address (str): Endereço IP e porta da câmera no formato "IP:Porta".
        """
        try:
            self.camera_source = f"http://{ip_address}/video"
            print(f"Câmera IP em {ip_address} configurada com sucesso!")
        except Exception as e:
            print(f"Erro ao configurar a câmera IP: {e}")

    def recognize(self):
        if hasattr(self, 'camera_source'):
            cap = cv2.VideoCapture(self.camera_source)
        else:
            cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise Exception("Erro ao abrir a câmera.")

        while True:
            name = input("Nome da pessoa: ")
            if not name:
                continue

            person_folder = os.path.join(self.training_data_dir, name)
            if not os.path.exists(person_folder):
                os.makedirs(person_folder)

            start_time = time.time()
            count = 0

            while time.time() - start_time < self.training_duration:
                elapsed_time = time.time() - start_time
                remaining_time = self.training_duration - elapsed_time
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                timer_text = f'Tempo restante: {minutes:02}:{seconds:02}'

                ret, frame = cap.read()
                if not ret:
                    print("Erro ao capturar o frame da câmera")
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)

                cv2.imshow('Capturando rosto...', frame)

                img_pil = Image.fromarray(frame)
                print(f"Dimensões da imagem: {img_pil.size}")
                print(f"Modo de cores: {img_pil.mode}")

                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))

                for (x, y, w, h) in faces:
                    aspect_ratio = w / h
                    if 0.8 <= aspect_ratio <= 1.2:
                        roi_gray = gray[y:y + h, x:x + w]
                        resized_face = cv2.resize(roi_gray, (200, 200))
                        resized_face = cv2.equalizeHist(resized_face)

                        image_path = os.path.join(person_folder, f'{name}_{count}.png')
                        cv2.imwrite(image_path, resized_face)
                        count += 1

                        time.sleep(0.1)

                cv2.putText(frame, timer_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            print(f"{name} salvo com sucesso!")

            choice = input("Deseja treinar outra pessoa? (1 - Sim, 2 - Não): ")
            if choice == '2':
                break

        cap.release()
        cv2.destroyAllWindows()

        self.load_training_data()
        self.model = self.create_model()
        self.train_model()
        print("Modelo treinado e salvo com sucesso!")

    def start(self):
        if hasattr(self, 'camera_source'):
            cap = cv2.VideoCapture(self.camera_source)
        else:
            cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise Exception("Erro ao abrir a câmera.")

        while True:
            ret, frame = cap.read()

            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)

                cv2.imshow('Câmera', frame)

                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=6)

                for (x, y, w, h) in faces:
                    roi_color = rgb_frame[y:y + h, x:x + w]
                    roi_gray = cv2.resize(roi_color, (200, 200))
                    roi_gray = cv2.cvtColor(roi_gray, cv2.COLOR_RGB2GRAY)
                    roi_gray = roi_gray / 255.0
                    roi_gray = roi_gray.reshape(1, 200, 200, 1)

                    prediction = self.model.predict(roi_gray, verbose=0)

                    label_id = np.argmax(prediction)

                    # Verifica a confiança da predição (acima de 50%)
                    if 0 <= label_id < len(self.labels) and prediction[0][label_id] > 0.7: 
                        label = list(self.labels.keys())[label_id]
                        confidence = prediction[0][label_id] * 100
                        label_with_confidence = f"{label} {confidence:.2f}%"
                    else:
                        label = "Desconhecido"
                        label_with_confidence = "Desconhecido"
                        print("Não reconhecido")

                    cv2.putText(rgb_frame, label_with_confidence, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    print(f"Pessoa reconhecida: {label}")

                frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                cv2.imshow('Câmera', frame)

            else:
                print("Erro ao ler o frame da câmera.")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()