$(".image-checkbox").each(function () {
  if ($(this).find('input[type="checkbox"]').first().attr("checked")) {
    $(this).addClass("image-checkbox-checked");
  } else {
    $(this).removeClass("image-checkbox-checked");
  }
});

// sync the state to the input
$(".image-checkbox").on("click", function (e) {
  $(this).toggleClass("image-checkbox-checked");
  var $checkbox = $(this).find('input[type="checkbox"]');
  $checkbox.prop("checked", !$checkbox.prop("checked"));

  e.preventDefault();
});

$(document).ready(function () {
  $("#overlay").hide();

  const runPyScript = (image_path, overlay_image) => {
    return new Promise((resolve, reject) => {
      let formData = new FormData();
      formData.append("overlay_image", overlay_image, overlay_image.name);
      formData.append("image_path", image_path);

      $.ajax({
        method: "POST",
        url: "/change_image",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
          resolve(data);
        },
        error: function (xhr, textStatus, errorThrown) {
          reject(errorThrown);
        },
      });
    });
  };

  const addOverlay = async () => {
    const selectedImage = document.getElementById("imageUpload").files[0];

    if (selectedImage) {
      $("#overlay").show();

      let checkedImagesLabels = document.getElementsByClassName(
        "image-checkbox-checked"
      );

      for (let i = 0; i < checkedImagesLabels.length; i++) {
        let image = checkedImagesLabels[i].getElementsByTagName("img")[0];
        let imgSrc = image.src;

        if (imgSrc.includes("?")) {
          imgSrc = imgSrc.split("?")[0];
        }
        console.log(imgSrc);

        try {
          const new_image_path = await runPyScript(imgSrc, selectedImage);
          console.log(new_image_path);

          $(image).attr({
            src: `${new_image_path}?t=${new Date().getTime()}`,
          });
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      }

      $("#overlay").hide();
    }
  };

  $("#imageUpload").on("input", addOverlay);
  $("#imagesUpdate").on("click", addOverlay);
  $("#imagesReset").on("click", () => window.location.reload());
});
