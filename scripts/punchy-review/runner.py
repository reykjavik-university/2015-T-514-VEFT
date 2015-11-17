import part1
import part2
import part3
import part4
import part5
import part6

# Tune these parameters.
url_prefix = 'http://localhost:4000'
admin_token = 'changeme'

if __name__ == '__main__':
    parts = [part1.Test, part2.Test, part3.Test, part4.Test, part5.Test, part6.Test]
    total_score = 0

    for part in parts:
        print part.__doc__
        try:
            part_score = part(base_url=url_prefix, admin_token=admin_token).execute()
        except Exception as ex:
            print ex
            part_score = 0
        print 'score:', part_score
        total_score += part_score
        print '==================================='

    print 'Total score:', total_score
