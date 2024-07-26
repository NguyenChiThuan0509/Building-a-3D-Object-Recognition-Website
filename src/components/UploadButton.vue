<template>
    <div class="div-upload">
        <input type="file" @change="handleFileUpload" ref="fileInput" style="display: none" />
        <button @click="triggerFileInput">Upload Image/Video</button>
        <div v-if="fileUrl" class="upload-btn">
            <img v-if="isImage" :src="fileUrl" alt="Uploaded Image" style="max-width: 100%; height: auto;" />
            <video v-if="isVideo" controls :src="fileUrl" style="max-width: 100%; height: auto;"></video>
        </div>
        <div v-if="loadingMessage">{{ loadingMessage }}</div>
        <div v-if="errorMessage" style="color: red;">{{ errorMessage }}</div>
        <div v-if="resultUrl" class="detect-result">
            <h2>Detection Result:</h2>
            <img :src="resultUrl" alt="Detection Result" style="max-width: 100%; height: auto;" />
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            fileUrl: null,
            resultUrl: null,
            isImage: false,
            isVideo: false,
            loadingMessage: '',
            errorMessage: ''
        };
    },
    methods: {
        triggerFileInput() {
            this.$refs.fileInput.click();
        },
        async handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.fileUrl = URL.createObjectURL(file);
                this.isImage = file.type.startsWith('image/');
                this.isVideo = file.type.startsWith('video/');

                // Send the file to the backend for detection
                const formData = new FormData();
                formData.append("file", file);

                this.loadingMessage = 'Chờ trong giây lát!';
                this.errorMessage = '';

                try {
                    const response = await fetch('http://127.0.0.1:8000/detect/', {
                        method: 'POST',
                        body: formData
                    });

                    if (response.ok) {
                        const blob = await response.blob();
                        this.resultUrl = URL.createObjectURL(blob);
                        this.loadingMessage = '';
                    } else {
                        const errorData = await response.json();
                        this.errorMessage = errorData.message || 'Detection failed';
                        this.loadingMessage = '';
                    }
                } catch (error) {
                    this.errorMessage = 'Error uploading file: ' + error.message;
                    this.loadingMessage = '';
                }
            }
        }
    }
};
</script>

<style scoped>
.div-upload {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.upload-btn,
.detect-result {
    max-width: 700px;
    max-height: 700px;
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

img,
video {
    margin-top: 20px;
}
</style>
