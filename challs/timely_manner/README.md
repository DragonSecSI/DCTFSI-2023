# Timely manner

> 2023-03-29, author: [medic](https://github.com/aljazmedic)

## Idea

To demonstrate why using

```php
srand(float(time()));
```

is not a good idea.

## Usage

```bash
# Preparation
cp .env.example .env
# And then change the values

# To bring containers up
docker-compose up

# To bring them down
docker-compose down
```

## Exploitation

Becaus php is seeded by `time()`, which is predictable per-request, we can roughly estimate `time()` with our own php script and then try values around the estimation. (+/- 1 second). Then we seed our own random and execute the prediction.

Solution [here](/exploit.php).
