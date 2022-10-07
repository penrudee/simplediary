window.onload = function() {
	var embedo=new Embedo({facebook:{version:"v8.0",appId:"180015362652616",access_token:"180015362652616|fb4b1e9203a607f5e9d9d49c666ee200",xfbml:!0},twitter:!0,instagram:{access_token:"180015362652616|fb4b1e9203a607f5e9d9d49c666ee200"},pinterest:!0});
	

	embedo
		.load(
			document.getElementById("embedo-twitter"),
			"https://twitter.com/Sh0bhit/status/797584590214926340"
		)
		.done(function() {
			console.log("Tweet Loaded. [hide loader if/any]");
		});

	embedo.load(
		document.getElementById("embedo-instagram"),
		"https://www.instagram.com/p/BJA9BB-B46A",
		{
			hidecaption: false
		}
	);

	embedo.load(
		document.getElementById("embedo-pinterest-pin"),
		"https://www.pinterest.com/pin/99360735500167749"
	);

	embedo.load(
		document.getElementById("embedo-youtube-embed"),
		"https://www.youtube.com/embed/vn2qXpcon-s",
		{
			width: '100%',
			height: 480
		}
	);
};
