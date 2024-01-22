# Convection Plugin - Secrets - Generic

- [Convection Plugin - Secrets - Generic](#convection-plugin---secrets---generic)
  - [Physical Storage](#physical-storage)
    - [Data Format](#data-format)
  - [Secret Store Args](#secret-store-args)
    - [***TBD***](#tbd)
  - [Secrets Args](#secrets-args)
    - [Create/Modify](#createmodify)
    - [Get/Destroy](#getdestroy)

Generic Secrets Storage (Key/Value Store)

## Physical Storage

If the Secret Store Name contains slashes, it is assumed as a path, and placed as `$STORAGE_ROOT/$STORE_NAME` (ex: `(/data)/(my/secret/store)`). If it does not contain slashes, it is stored at `$STORAGE_ROOT/secrets/$STORE_NAME` (ex `(/data)/(my.secret.store)`)

Data is stored all in a single file.

### Data Format

```json
{
    "metadata": { <plugin metadata> },
    "config": { <configuration data> },
    "store": { <secrets in k:v form>},
    "stats": {
        "reads": <number of reads performed since creation>,
        "writes": <number of writes performed since creation>
    }
}
```

Note that the Stats data for Reads may not be accurately represented if a number reads happen, but a write does not occur before the Convection Secrets Manager is shutdown/restarted. These stats are held in memory until a write occurs, and so the stat for reads since the last write would be lost on stop/restart. Write stat should always be accurate. The Read stat will be accurate for the duration of the service running (assuming no writes), however.

## Secret Store Args

These arguments are required when a new Generic Store is created.

### ***TBD***

## Secrets Args

### Create/Modify

 - `secret_name`: Name of Secret to Create/Modify
 - `secret_value`: Secret Data

### Get/Destroy

 - `secret_name`: Name of Secret to View/Destroy

