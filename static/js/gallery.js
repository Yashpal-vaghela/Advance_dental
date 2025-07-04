/*----------------------------------------------------*/
  /*	Gallery Image Grid
  /*----------------------------------------------------*/
  $(".grid-loaded").imagesLoaded(function () {
    // filter items on button click
    $(".gallery-filter").on("click", "button", function () {
      var filterValue = $(this).attr("data-filter");
      $grid.isotope({
        filter: filterValue,
      });
    });
    // change is-checked class on buttons
    $(".gallery-filter button").on("click", function () {
      $(".gallery-filter button").removeClass("is-checked");
      $(this).addClass("is-checked");
      var selector = $(this).attr("data-filter");
      $grid.isotope({
        filter: selector,
      });
      return false;
    });

    // init Isotope
    var $grid = $(".masonry-wrap").isotope({
      itemSelector: ".gallery-item",
      percentPosition: true,
      transitionDuration: "0.7s",
      masonry: {
        // use outer width of grid-sizer for columnWidth
        columnWidth: ".gallery-item",
      },
    });
  });
  /*----------------------------------------------------*/
  /*	Single Image Lightbox
  /*----------------------------------------------------*/
  $(".image-link").magnificPopup({
    type: "image",
  });