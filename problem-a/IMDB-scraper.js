// const request = require("request");
// const cheerio = require("cheerio");
// const fs = require("fs"); //file system
// const express = require("express");

// var title,release,rating
// var json={title:"",release:"",rating:""}
// const app=express()
// app.get('/scrape',(req,res)=>{
//   //scraping code
//   base_url="https://www.imdb.com/"
//   movieTitle="chart/top/?ref_=nv_mv_250"
//   // url="https://www.imdb.com/chart/top/?ref_=nv_mv_250"
//   review="reviews?ref_=tt_urv"
//   request(base_url+movieTitle,function(error1,response1,html1){
//     var $1=cheerio.load(html1)
//     const topMovies = [];
//     $1('.ipc-title-link-wrapper').each((index1, element1) => {
//       if (index1 < 20) {
//         const title = $1(element1).text().trim();
//         const link = $1(element1).attr('href').split('?');
//         const url=base_url+link[0]+review
//         var reviewList=[]
//         request(url,function(error2,response2,html2){
//           var $2=cheerio.load(html2)
//           $2('.content').filter(function(){
//             var data2=$2(this)
//             content=data2.text()
//             reviewList.push({content})
//             console.log(content);
//           })
//           // $2('content').each((index2,element2)=>{
//           //   if(index2<10){
//           //     const content=$2(element2).text().trim()
//           //     console.log(content)
//           //     // reviewList.push({content})
//           //   }
//           })
//         })
//         topMovies.push({ title, reviewList});
//       }
//     });
//     // console.log(topMovies)
//     res.json(topMovies)
//   })
// })
// app.listen(5000,function(){
//   console.log("Server is listening on Port 5000")
// })

// chatgpt
const request = require("request");
const cheerio = require("cheerio");
const express = require("express");

const app = express();

app.get('/scrape', async (req, res) => {
  const base_url = "https://www.imdb.com/";
  const movieTitle = "chart/top/?ref_=nv_mv_250";
  const review = "reviews/?ref_=tt_ql_2";

  const getReviews = async (url) => {
    return new Promise((resolve, reject) => {
      request(url, (error2, response2, html2) => {
        if (error2 || response2.statusCode !== 200) {
          reject(error2 || `Error fetching reviews: Status Code ${response2.statusCode}`);
        } else {
          const $2 = cheerio.load(html2);
          const reviewList = [];

          $2('.text.show-more__control').each((index2, element2) => {
            if (index2 < 10) {
              const content = $2(element2).text().trim();
              reviewList.push({ content });
            }
          });

          resolve(reviewList);
        }
      });
    });
  };

  request(base_url + movieTitle, async (error1, response1, html1) => {
    if (error1 || response1.statusCode !== 200) {
      console.error('Error fetching top movies:', error1);
      res.status(500).send('Internal Server Error');
      return;
    }

    const $1 = cheerio.load(html1);
    const topMovies = [];

    const processMovie = async (index1, element1) => {
      const title = $1(element1).text().trim();
      const link = $1(element1).attr('href').split('?');
      const url = base_url + link[0] + review;

      try {
        const reviewList = await getReviews(url);
        topMovies.push({ title, reviewList });

        if (topMovies.length === 20) {
          res.json(topMovies);
        }
      } catch (error2) {
        console.error('Error fetching reviews:', error2);
      }
    };

    $1('.ipc-title-link-wrapper').slice(0, 20).each(processMovie);
  });
});

app.listen(5000, () => {
  console.log("Server is listening on Port 5000");
});


