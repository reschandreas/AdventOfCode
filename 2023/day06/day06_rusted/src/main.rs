fn get_numbers_from_line(line: &str, prefix: &str) -> Vec<u64> {
    line.strip_prefix(prefix)
        .unwrap()
        .split_whitespace()
        .flat_map(str::parse::<u64>)
        .collect()
}

fn get_number_from_line(line: &str, prefix: &str) -> u64 {
    let number = line.strip_prefix(prefix)
        .unwrap()
        .replace(" ", "");
    number.parse::<u64>().unwrap()
}

fn main() {
//     let mut input = String::from("Time:      7  15   30
// Distance:  9  40  200");
    let input = String::from("Time:        50     74     86     85
Distance:   242   1017   1691   1252");
    let mut lines = input.lines();
    let timeline = lines.next().unwrap();
    let distanceline = lines.next().unwrap();
    let mut times: Vec<u64> = get_numbers_from_line(timeline, "Time:");
    times.clear();
    times.push(get_number_from_line(timeline, "Time:"));
    let mut distances: Vec<u64> = get_numbers_from_line(distanceline, "Distance:");
    distances.clear();
    distances.push(get_number_from_line(distanceline, "Distance:"));
    println!("times: {:?}", times);
    println!("distances: {:?}", distances);
    let mut vec: Vec<u64> = Vec::new();
    times.iter().zip(distances.iter()).for_each(|(time, distance)| {
        let mut vec2: Vec<u64> = Vec::new();
        for i in 1..*time {
            let pushed: u64 = i;
            let remaining: u64 = *time - pushed;
            let traveled: u64 = pushed * remaining;
            if traveled > *distance {
                vec2.push(pushed);
            }
        }
        vec.push(vec2.len() as u64);
    });
    let products = vec.iter().product::<u64>();
    println!("products: {:?}", products);
}
