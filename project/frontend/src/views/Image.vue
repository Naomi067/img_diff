<template>
    <div class="image">
        <NaviTop> </NaviTop>
        <el-container>
            <ImageUpload> </ImageUpload>
            <ImageUploadDiff> </ImageUploadDiff>
        </el-container>
    </div>

</template>

<script>
    import NaviTop from '@/components/NaviTop.vue'
    import ImageUpload from '@/components/ImageUpload.vue'
    import ImageUploadDiff from '@/components/ImageUploadDiff.vue'
    
    export default {
        name: 'Image',
        components: {
            NaviTop,
            ImageUpload,
            ImageUploadDiff
        }
    }
</script>