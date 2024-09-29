const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function scrapeQuotes() {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  // Navigate to the login page
  await page.goto('https://quotes.toscrape.com/login');

  // Enter login credentials
  await page.type('input[name="username"]', 'admin');
  await page.type('input[name="password"]', 'admin');
  await page.click('input[type="submit"]');

  // Wait for navigation to complete after login
  await page.waitForNavigation();

  // Check if login was successful
  console.log(page.url())
  if (page.url() !== 'https://quotes.toscrape.com/') {
    console.error('Login failed!');
    await browser.close();
    return;
  }

  console.log('Logged in successfully!');

  let allQuotes = [];

  // Loop through all 10 pages
  for (let i = 1; i <= 10; i++) {
    console.log(`Scraping page ${i}...`);
    await page.goto(`https://quotes.toscrape.com/page/${i}/`);

    // Scrape quotes on the current page
    const quotesOnPage = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('.quote')).map(quote => ({
        text: quote.querySelector('.text').innerText,
        author: quote.querySelector('.author').innerText,
        authorLink: quote.querySelector('a[href*="goodreads"]').href,  
        tags: Array.from(quote.querySelectorAll('.tag')).map(tag => tag.innerText)
      }));
    });

    // Append current page's quotes to the allQuotes array
    allQuotes = allQuotes.concat(quotesOnPage);
  }

  await browser.close();

  // Save the scraped quotes to a JSON file
  const filePath = path.join(__dirname, '../data/quotes.json');
  fs.writeFileSync(filePath, JSON.stringify(allQuotes, null, 2));
  console.log(`Scraped ${allQuotes.length} quotes and saved them to ${filePath}`);
}

scrapeQuotes().catch(err => console.error('Error scraping quotes:', err));
