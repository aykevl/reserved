# Check common mailbox and user names

When you let users of a webapp create their own usernames, and this name is used
in an email address or Unix user, it is important to check against some common
usernames, like 'root', 'postmaster', and 'postfix'. This library is an attempt
for that.

You should check the following:
  * The address in your WHOIS, wich may be used for things like registering a
    TLS certificate. It should really be something like hostmaster@ anyway, so
    this *should not* be an issue.
  * If you make Unix accounts with these names, check which names occur in
    `/etc/passwd` (and possibly `/etc/shadow`).

License: BSD 2-clause

Resources:

  * [RFC2142](https://www.ietf.org/rfc/rfc2142.txt)
  * [Security StackExchange: What email addresses are treated as trusted?](http://security.stackexchange.com/questions/84127/what-email-addresses-are-treated-as-trusted)
  * [Postbit reserved username list](http://blog.postbit.com/reserved-username-list.html)
  * `/etc/passwd` and `/etc/group` on my laptop (Debian testing/stretch).
  * [shouldbee's list](https://github.com/shouldbee/reserved-usernames)
  * [kwappa's list](https://github.com/kwappa/username_not_reserved_validator/blob/master/lib/username_not_reserved_validator/reserved_names.rb)

![Exploits of a Mom](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)
([via xkcd.com](https://xkcd.com/327/))
