$('#profile-image-file').on('change', function() {
   if (this.files && this.files[0]) {
      var reader = new FileReader();
      reader.onload = (e)=> {
            $('#profile-image-src').attr('src', e.target.result);
      }
      reader.readAsDataURL(this.files[0]);
   }
});