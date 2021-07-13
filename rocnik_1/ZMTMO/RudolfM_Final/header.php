<?php 
	include 'funkcia.php';
 ?>
<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" type="text/css" href="css/style.css">
	<meta charset="utf-8">
	<title>hardware</title>
</head>
<body>
	<header>
		<div class="jazyk">
			<a  href="homepage.php?lang=sk">SVK/</a>
			<a  href="homepage.php?lang=en">EN</a>
		</div>
			<ul>
			<li><a class="navigacia" href="homepage.php"><img class="logo" src="images/logo4.svg" alt="logo"></a></li>
			<li><a href="homepage.php"><?php echo $lang['homepage'] ; ?></a></li>
			<li><a href="funkcie.php"><?php echo $lang['funkcie'] ; ?></a></li>
	 		<li><a href="hardware.php"><?php echo $lang['hardware'] ; ?></a></li>
			<li><a href="prislusenstvo.php"><?php echo $lang['prislusenstvo'] ; ?></a></li>
			<li><a href="oprava.php"><?php echo $lang['oprava'] ; ?></a></li>
			<li><a href="galeria.php"><?php echo $lang['galeria'] ; ?></a></li>
			<li><a href="inemodely.php"><?php echo $lang['inemodely'] ; ?></a></li>
			<li><a href="onas.php"><?php echo $lang['onas'] ; ?></a></li>
			<li><form action="#" method="get" role="search">
					<input class="search" type="search" name="hladaj" placeholder="search">
				</form>
			</li>
			<?php  
				/*echo  "";
				
				if ($page_name == 'homepage') echo '<li><strong>Hlavná stránka</strong></li>';
					else echo "<li><a href="homepage.php">Hlavná stránka</a></li>";

				if ($page_name == 'funkcie') echo '<li><strong>Funkcie</strong></li>';
					else echo "<li><a href="funkcie.php">Funkcie</a></li>";
		 		
		 		if ($page_name == 'hardware') echo '<li><strong>Hardware</strong></li>';
		 			else echo "<li><a href="hardware.php">Hardware</a></li>";
				
				if ($page_name == 'prislusenstvo') echo '<li><strong>Príslušenstvo</strong></li>';
					else echo "<li><a href="prislusenstvo.php">Príslušenstvo</a></li>";
				
				if ($page_name == 'oprava') echo '<li><strong>Oprava</strong></li>';
					else echo "<li><a href="oprava.php">Oprava</a></li>";
				
				if ($page_name == 'galeria') echo '<li><strong>Galéria</strong></li>';
					else echo "<li><a href="galeria.php">Galéria</a></li>";
				
				if ($page_name == 'ine modely') echo '<li><strong>Iné Modely</strong></li>';
					else echo "<li><a href="ine%20modely.php">Iné modely</a></li>";

				if ($page_name == 'o nas') echo '<li><strong>O nás</strong></li>';
					else echo "<li><a href="o%20nas.php">O nás</a></li>";
				
				echo "<li><form action="" method="get" role="search">
							  <input class="search" type="search" name="hladaj" placeholder="search">
						  </form>
					  </li>";*/
			?>
			</ul>
	</header>