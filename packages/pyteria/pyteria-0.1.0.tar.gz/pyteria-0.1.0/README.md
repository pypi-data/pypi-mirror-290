<div align="center">
    <img width="96" src="./assets/pyteria.png"><br>
    <h1>Pyteria</h1>
</div>

# Example

```python
import asyncio
import soteria

async def main():
    cache = soteria.MemoryCache()
    client = soteria.Client(auth="<TOKEN HERE>", cache=cache)

    # fetch a user from the api
    user = await soteria.User.fetch(client, 12345)
    print(user)

    # fetch the list of followers
    followers = await user.fetch_followers()
    print(followers)

    # you can always access the cached list of followers if async is not allowed
    print(user.followers)

    # remember to close the client after execution
    await client.close()

asyncio.run(main())
```

# Features

- Mostly complete coverage of the Soteria API.
- Caching support with customiziable cache implementations.
- Complete type safety with your favorite type checker. 🚀
