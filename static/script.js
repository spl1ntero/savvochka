$(document).ready(function() {
  $.ajax({
    url: '/get_flowers',
    method: 'GET',
    success: function(response) {
      displayFlowers(response);
    },
    error: function(xhr, status, error) {
      console.error(xhr.responseText);
    }
  });

  function displayFlowers(flowers) {
    var flowersList = $('#flowersList');
    flowersList.empty();
    $.each(flowers, function(index, flower) {
      var flowerRow = $('<tr class="flower-row"></tr>');
      flowerRow.append('<td>' + flower.name + '</td>');
      flowerRow.append('<td>' + flower.type + '</td>');
      flowerRow.append('<td>' + flower.country + '</td>');
      flowerRow.append('<td>' + flower.season + '</td>');
      flowerRow.append('<td>' + flower.sort + '</td>');
      flowerRow.append('<td>' + flower.price + '</td>');
      flowersList.append(flowerRow);
    });
  }

  $.ajax({
    url: '/get_suppliers',
    method: 'GET',
    success: function(response) {
      displaySuppliers(response);
    },
    error: function(xhr, status, error) {
      console.error(xhr.responseText);
    }
  });

  function displaySuppliers(suppliers) {
    var suppliersList = $('#suppliersList');
    suppliersList.empty();
    $.each(suppliers, function(index, supplier) {
      var supplierRow = $('<tr></tr>');
      supplierRow.append('<td>' + supplier.name + '</td>');
      supplierRow.append('<td>' + supplier.type + '</td>');
      supplierRow.append('<td>' + supplier.address + '</td>');
      suppliersList.append(supplierRow);
    });
  }

  $.ajax({
    url: '/get_sellers',
    method: 'GET',
    success: function(response) {
      displaySellers(response);
    },
    error: function(xhr, status, error) {
      console.error(xhr.responseText);
    }
  });

  function displaySellers(sellers) {
    var sellersList = $('#sellersList');
    sellersList.empty();
    $.each(sellers, function(index, seller) {
      var sellerRow = $('<tr></tr>');
      sellerRow.append('<td>' + seller.name + '</td>');
      sellerRow.append('<td>' + seller.address + '</td>');
      sellersList.append(sellerRow);
    });
  }

  function addSeller() {
    var name = $('#sellerNameInput').val();
    var address = $('#sellerAddressInput').val();

    $.ajax({
      url: '/add_seller',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({name: name, address: address}),
      success: function(response) {
        displaySellers(response);
        $('#sellerNameInput').val('');
        $('#sellerAddressInput').val('');
      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  }

  function getFlowersBySeason() {
    var season = $('#seasonSelect').val();
    $.ajax({
      url: '/filter_by_season/' + season,
      method: 'GET',
      success: function(response) {
        displayFlowers(response);
      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  }

  function getFlowersByCountry() {
    var country = $('#countryInput').val();
    $.ajax({
      url: '/filter_by_country/' + country,
      method: 'GET',
      success: function(response) {
        displayFlowers(response);
      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  }
});
