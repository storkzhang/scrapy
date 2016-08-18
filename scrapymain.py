import json
import scrapy
import sys


class LoginSpider(scrapy.Spider):
    handle_httpstatus_list = [401]
    name = 'loginspider'
    start_urls = ["your site"]
    log_url = "your log site"
    username = "your name"
    password = "your password"

    def parse(self, response):
        return scrapy.FormRequest.from_response(
                response,
                formdata={'username': self.username, 'password': self.password},
                callback=self.after_login
                )

    def after_login(self, response):
        yield {"login status:": response}
        yield scrapy.Request(response.urljoin(self.log_url), self.parse_log, dont_filter=True)


    def parse_log(self, response):
        reload(sys)
        sys.setdefaultencoding( "utf-8" )
        log_content = response.body_as_unicode()
        log_content = log_content.replace(")]}'", "")
        yield {"log_content":log_content}
        log_json = json.loads(log_content)
        f = open("alpha_chagne_2016-08-17.html", "wb")
        f.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body><table border="1"><tbody><tr><td>Related JIRA</td><td>Subject</td><td>Status</td><td>Owner</td><td>Project</td><td>Branch</td><td>Updated</td></tr>')
        for log_item in log_json:
            f.write("<tr>")
            f.write("<td>")

            for k,v in log_item['revisions'].iteritems():
                f.write(v['commit']['message'].split('\n\n')[1])
                self.email = v['commit']['committer']['email']
                break;
            f.write("</td>")

            f.write("<td>"+log_item['subject']+"</td>")
            f.write("<td>"+log_item['status']+"</td>")
            f.write("<td>"+self.email+"</td>")
            f.write("<td>"+log_item['project']+"</td>")
            f.write("<td>"+log_item['branch']+"</td>")
            f.write("<td>"+log_item['updated']+"</td>")
            f.write("</tr>")
        f.write("</tbody></table></body></html>")
        f.close()
