<template>
    <div>
        <Header />
        <!-- <UploadButton /> -->
        <VideoPlayer />
        <div class="div-detect-image">
            <button @click="detectImage">Detect Image</button>
            <div v-if="resultImageUrl">
                <h2>Detection Result:</h2>
                <img :src="resultImageUrl" alt="Detection Result" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Header from '@/components/Header.vue'
import VideoPlayer from '@/components/VideoPlayer.vue'
// import UploadButton from '@/components/UploadButton.vue'

export default {
    name: 'Home',
    components: {
        Header,
        VideoPlayer,
        // UploadButton
    },
    data() {
        return {
            resultImageUrl: null
        }
    },
    methods: {
        async detectImage() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/detect-image', { responseType: 'blob' });
                this.resultImageUrl = URL.createObjectURL(response.data);
            } catch (error) {
                console.error("Error detecting image:", error);
            }
        }
    }
}
</script>

<style scoped>
.div-detect-image {
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
</style>
