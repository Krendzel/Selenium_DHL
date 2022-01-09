# Selenium DHL

Simple python script that uses Selenium to fix wrong postal codes in files that create shipments in DHL by another API.
If you want to use it, you need to have a DHL account.
After processing the file, it will move processed file with the fixed postal codes. to another folder. (defined in `.env` file)

## Prerequisites

### Selenium WebDriver

Download WebDrivers:
* [Firefox Driver](https://github.com/mozilla/geckodriver/releases)
* [Chrome Driver](https://chromedriver.chromium.org/downloads)

Extract to drivers to: `C:/selenium_drivers`


Add directory with drivers to PATH:

```bash
#Powershell
$env:Path += ";C:\selenium_drivers"
```
### .env file
Change name of `env.example` to `.env` and add your credentials to DHL site.


## Usage
To run script use: `python main.py`

On first run you will be asked to create directories for files.
```bash
🔥 Checking directories...
Directory APP_IN/ does not exist. Create it? [y/n]
Directory APP_OUT/ does not exist. Create it? [y/n]
Directory APP_OUT/OLD/ does not exist. Create it? [y/n]
Directory APP_ERROR/ does not exist. Create it? [y/n]
```

After init you can run script again to start processing.
You need `*.xml` files in `APP_IN` that script will parse.

Example .xml file:

```xml
<?xml version='1.0' encoding='utf-8'?>
<Shipment>
	<order>CXL7450948</order>
	<name>Karol Królczyk</name>
	<street>Bociania</street>
	<houseNumber>63</houseNumber>
	<country>Polska</country>
	<postalCode>65-497</postalCode>
	<city>Bielsko-Biała</city>
</Shipment>
```
This example is provided by Faker library.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## TODO

* [ ] Add ability to use another driver (currently only Chrome)
* [ ] Catch exceptions and move file to `APP_ERROR`
* [ ] Add ability to use another file (currently only .xml)


## License
[MIT](https://choosealicense.com/licenses/mit/)