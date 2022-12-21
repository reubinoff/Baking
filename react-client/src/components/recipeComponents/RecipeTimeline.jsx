import Timeline from "@mui/lab/Timeline";
import TimelineItem from "@mui/lab/TimelineItem";
import TimelineSeparator from "@mui/lab/TimelineSeparator";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineContent, {
  timelineContentClasses,
} from "@mui/lab/TimelineContent";
import timelineItemClasses from "@mui/lab/TimelineItem";
import TimelineDot from "@mui/lab/TimelineDot";
import { PropTypes } from 'prop-types';
import TimelineOppositeContent from "@mui/lab/TimelineOppositeContent";
export default function RecipeTimeline(props) {
    const { items } = props;
  return (
    <Timeline {...props}>
      {items.map((item) => (
        <TimelineItem key={item.val}>
          <TimelineOppositeContent> {item.val} </TimelineOppositeContent>
          <TimelineSeparator>
            <TimelineDot variant={item.main ? "default" : "outlined"} />
            <TimelineConnector
              sx={{ display: item.connector === true ? "flex" : "none" }}
            />
          </TimelineSeparator>
        </TimelineItem>
      ))}
    </Timeline>
  );
}

RecipeTimeline.propTypes = {
    items: PropTypes.array.isRequired,
}

// items = [
//     {
//         val: "Step 1",
//         main: false,
//         connector: true,
//     }
// ]
