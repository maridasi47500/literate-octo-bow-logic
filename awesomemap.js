var theme = 'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png';
const LeafIcon = L.Icon.extend({
			options: {
							iconSize:     [95, 95],
							shadowSize:   [50, 54],
							iconAnchor:   [50, 50],
							shadowAnchor: [50, 62],
							popupAnchor:  [25, 25]
						}
		});

    var lat = 8.619543;
        var lon = 0.82;
            var alt =481;
                var macarte = null;
                    //var trace = new Array();
                        var i = 0;
                            //var marker1;
                                var markerClusters; // Servira à stocker les groupes de marqueurs
                                    var popup = L.popup();
                                      function initMap(){

                                            // Nous définissons le dossier qui contiendra les marqueurs
                                                  //var iconBase = 'img';
                                                        // Créer l'objet "macarte" et l'insèrer dans l'élément HTML qui a l'ID "map"
                                                              macarte = L.map('map').setView([lat, lon], 5);

                                                                    markerClusters = L.markerClusterGroup; // Nous initialisons les groupes de marqueurs
                                                                          // Leaflet ne récupère pas les cartes (tiles) sur un serveur par défaut. Nous devons lui préciser où nous souhaitons les récupérer. Ici, openstreetmap.fr
                                                                                L.tileLayer(theme, {
                                                                                          // Il est toujours bien de laisser le lien vers la source des données
                                                                                                    //attribution: 'données © OpenStreetMap/ODbL - rendu OSM France',
                                                                                                              minZoom: 1,
                                                                                                                        maxZoom: 20
                                                                                                                              }).addTo(macarte);
                                                                                                                                    macarte.on('click', onMapClick);
                                                                                                                                      }


   function onMapClick(e) {
           var mylat = document.getElementById("somefield{tablename}lat");
           var mylon = document.getElementById("somefield{tablename}lon");

	   if (document.getElementById("lat") && document.getElementById("lon")){
	       popup
	           .setLatLng(e.latlng)
	           .setContent("You clicked the map at " + e.latlng.toString())
	           .openOn(macarte);
	       var marker = L.marker(e.latlng).addTo(macarte)
	       mylat.value=e.latlng.lat;
	       mylon.value=e.latlng.lng;
	       console.log(e.latlng);
	   }
   }




                                                                                                                                                                                                      $(document).ready(function(){



                                                                                                                                                                                                              initMap();
                                              if (window.location.pathname==="/" || window.location.pathname==="/add_one_{tablename}"){
						      $.ajax({
							      url:"/voirtoutcequejaiajoute",
							      success: function(data){
								      var latlng,marker,tout=data.tout,hey,mypopup={},icon;
								      for(var i=0;i<tout.length;i++){
									      hey=tout[i];
 if ((window.location.pathname==="/alldatastorage" && hey.stuff !== "storage") || (window.location.pathname==="/allremedes" && hey.stuff !== "remede") || (window.location.pathname==="/allmynews" && hey.stuff !== "news")){
    continue;
 }

                                                                              mypopup[i] = L.popup();
									      latlng={
										          "lat": Number(hey.lat),
										          "lng": Number(hey.lon) 
									      };
									      console.log(latlng);
	                                                                      mypopup[i]
	                                                                          .setLatLng(latlng)
	                                                                          .setContent("1 "+hey.stuff+" apparait sur la carte a " + latlng.lat+" "+latlng.lng+"("+hey.content+")")
	                                                                          .openOn(macarte);
									      icon=new LeafIcon({iconUrl: "/mypic/"+hey.stuff+".png"});
	                                                                      mymarker = L.marker(latlng, {icon: icon}).bindPopup(mypopup[i]).addTo(macarte)
								      }
							      }
						      });

if (document.getElementById("loadmycity")){
$('button#loadmycity').on('click', function () {
    var fData = new FormData();
    fData.append("job", monjob1.value);
    fData.append("lieu", monlieu1.value);
    fData.append("rayon", monrayon1.value);
    fData.append("sendemail", "anonyme@email.com");
    console.log("job", monjob1.value);
    console.log("lieu", monlieu1.value);
    console.log("rayon", monrayon1.value);
    console.log("sendemail", "anonyme@email.com");
    $.ajax({url:"/searchjobcity",


 type:"POST", 
 data:fData,
    cache: false,
    contentType: false,
    processData: false,

success:function(data){
    console.log(data);
    maregion1.value=data.region;
    var emplois=["departement","city","pays","region"];
    var myjob={};

    if (String(data["region"]) !== "undefined"){
        autresoffres.innerHTML ="";
        for (var y=0;y<emplois.length;y++){

            if (myjob[data[emplois[y]]] === undefined) {
                autresoffres.innerHTML +="<div onclick=\"chercherunjob.style.display='none';monjob1.value='';monlieu1.value='"+String(data[emplois[y]])+"';loadmycity.click();\" class=\"autreoption\">emploi à "+String(data[emplois[y]])+"</div>";
            }
            myjob[data[emplois[y]]]=emplois[y];
        }
        if (monjob1.value.length > 0){
            autresoffres.innerHTML +="<div onclick=\"chercherunjob.style.display='none';monlieu1.value='';monjob1.value='"+String(monjob1.value)+"';loadmycity.click();\" class=\"autreoption\">emploi en "+String(monjob1.value)+"</div>";
        }
    }

    maville1.value=data.ville;
    monpays1.value=data.pays; 
    moncode1.value=data.code;
    somefield{tablename}lat.value=data.latitude;
    somefield{tablename}lon.value=data.longitude;
    if (String(data.region) !== "undefined"){
    monadresse.innerHTML =String(data.region);
    monadresse.innerHTML +=", "+String(data.city);
    monadresse.innerHTML +=", "+String(data.pays);
    monadresse.innerHTML +=", "+String(data.code);
    monadresse.innerHTML +=", "+String(data.latitude);
    monadresse.innerHTML +=", "+String(data.longitude);
    }
    if (String(data.region) !== "undefined") {
       chercherunjob.style.display="block";
    }else{
       chercherunjob.style.display="none";
    }
    macarte.setView([parseFloat(data.latitude), parseFloat(data.longitude)], 5);


    }});
return false;
});
};
}
                                                                                                                                                                                                                  });
