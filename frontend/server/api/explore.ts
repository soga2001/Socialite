// import http 
import http from '../../assets/http';
import { Post } from '../../assets/interfaces';

export default defineEventHandler((event) => {
  console.log(event.node)
  // const data = await http.get('${backend_baseURL}/posts/explore/${this.user_timestap}/${this.page}/').then((res) => {
  //     console.log(res.data)
  //     return res.data
  // })
  return {
    hello: 'world'
  }
})