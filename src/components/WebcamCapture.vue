<template>
    <div class="webcam-container">
        <video ref="webcam" autoplay playsinline></video>
        <button @click="startDetection" :disabled="isDetecting">
            {{ isDetecting ? "Detecting..." : "Start Detection" }}
        </button>
        <canvas ref="canvas" style="display:none;"></canvas>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            isDetecting: false,
            errorMessage: '',
        };
    },
    mounted() {
        this.setupWebcam();
    },
    methods: {
        async setupWebcam() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                this.$refs.webcam.srcObject = stream;
            } catch (error) {
                console.error("Error accessing webcam: ", error);
            }
        },
        captureFrame() {
            const video = this.$refs.webcam;
            const canvas = this.$refs.canvas;
            const context = canvas.getContext("2d");

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            return new Promise((resolve) => {
                canvas.toBlob(resolve, 'image/jpeg');
            });
        },
        async startDetection() {
            this.isDetecting = true;
            this.errorMessage = '';

            while (this.isDetecting) {
                try {
                    const blob = await this.captureFrame();
                    const formData = new FormData();
                    formData.append('file', blob, 'webcam.jpg');

                    const response = await fetch('http://127.0.0.1:8000/detect/', {
                        method: 'POST',
                        body: formData
                    });

                    if (response.ok) {
                        const result = await response.json();
                        this.drawBoxes(result.boxes);
                    } else {
                        const errorData = await response.json();
                        this.errorMessage = errorData.message || 'Detection failed';
                        this.isDetecting = false;
                    }
                } catch (error) {
                    this.errorMessage = 'Error during detection: ' + error.message;
                    this.isDetecting = false;
                }
                await new Promise(resolve => setTimeout(resolve, 500)); // Adjust the delay as needed
            }
        },
        drawBoxes(boxes) {
            const video = this.$refs.webcam;
            const canvas = this.$refs.canvas;
            const context = canvas.getContext("2d");

            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            boxes.forEach(box => {
                context.beginPath();
                context.rect(box[0], box[1], box[2] - box[0], box[3] - box[1]);
                context.lineWidth = 2;
                context.strokeStyle = 'red';
                context.stroke();
            });
        }
    }
};
</script>

<style scoped>
.webcam-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

button {
    margin-top: 10px;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

button:disabled {
    background-color: #888;
    cursor: not-allowed;
}

video {
    width: 100%;
    max-width: 700px;
    height: auto;
    margin-top: 20px;
}

.error-message {
    color: red;
    margin-top: 10px;
}
</style>
