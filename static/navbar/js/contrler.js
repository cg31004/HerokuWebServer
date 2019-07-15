(function() {
		var menuEl = document.getElementById('ml-menu'),
			mlmenu = new MLMenu(menuEl, {
				// breadcrumbsCtrl : true, // show breadcrumbs
				// initialBreadcrumb : 'all', // initial breadcrumb text
				backCtrl : false, // show back button
				// itemsDelayInterval : 60, // delay between each menu item sliding animation
				onItemClick: loadDummyData // callback: item that doesn´t have a submenu gets clicked - onItemClick([event], [inner HTML of the clicked item])
			});

		// mobile menu toggle
		var openMenuCtrl = document.querySelector('.action--open'),
			closeMenuCtrl = document.querySelector('.action--close');

		openMenuCtrl.addEventListener('click', openMenu);
		closeMenuCtrl.addEventListener('click', closeMenu);

		function openMenu() {
			classie.add(menuEl, 'menu--open');
			closeMenuCtrl.focus();
		}

		function closeMenu() {
			classie.remove(menuEl, 'menu--open');
			openMenuCtrl.focus();
		}

		// simulate grid content loading
		var gridWrapper = document.querySelector('.content');

		function loadDummyData(ev, itemName) {
			ev.preventDefault();

			closeMenu();
			gridWrapper.innerHTML = '<img src=\"images/cthulu.png\"alt=\"Photo of Cthulu\"id=\"pic\"/><div id=\"contact-info\"class=\"vcard\"><!--Microformats!--><h1 class=\"fn\">蘇柏勳</h1><p>Email:<a class=\"email\"href=\"mailto:greatoldone@lovecraft.com\">cg3104@gmail.com</a></p></div><div id=\"objective\"><p>I am an outgoing and energetic(ask anybody)young professional,seeking a career that fits my professional skills,personality,and murderous tendencies.My squid-like head is a masterful problem solver and inspires fear in who gaze upon it.I can bring world domination to your organization.</p></div><div class=\"clear\"></div><dl><dd class=\"clear\"></dd><dt>Education</dt><dd><h2>Withering Madness University-Planet Vhoorl</h2><p><strong>Major:</strong>Public Relations<br/><strong>Minor:</strong>Scale Tending</p></dd><dd class=\"clear\"></dd><dt>Skills</dt><dd><h2>Office skills</h2><p>Office and records management,database administration,event organization,customer support,travel coordination</p><h2>Computer skills</h2><p>Microsoft productivity software(Word,Excel,etc),Adobe Creative Suite,Windows</p></dd><dd class=\"clear\"></dd><dt>Experience</dt><dd><h2>Doomsday Cult<span>Leader/Overlord-Baton Rogue,LA-1926-2010</span></h2><ul><li>Inspired and won highest peasant death competition among servants</li><li>Helped coordinate managers to grow cult following</li><li>Provided untimely deaths to all who opposed</li></ul><h2>The Watering Hole<span>Bartender/Server-Milwaukee,WI-2009</span></h2><ul><li>Worked on grass-roots promotional campaigns</li><li>Reduced theft and property damage percentages</li><li>Janitorial work,Laundry</li></ul></dd><dd class=\"clear\"></dd><dt>Hobbies</dt><dd>World Domination,Deep Sea Diving,Murder Most Foul</dd><dd class=\"clear\"></dd><dt>References</dt><dd>Available on request</dd><dd class=\"clear\"></dd></dl><div class=\"clear\"></div>';
			classie.add(gridWrapper, 'content--loading');
			setTimeout(function() {
				classie.remove(gridWrapper, 'content--loading');
				gridWrapper.innerHTML = '<ul class="products">' + dummyData[itemName] + '<ul>';
			}, 700);
		}
	})();